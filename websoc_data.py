import requests
from collections import defaultdict


BASE_URL = 'https://www.reg.uci.edu/perl/WebSoc'


def make_request(dept, course_num, year, qtr) -> (str, dict):
    qtr_num = None
    if qtr.upper() == 'FALL':
        qtr_num = '92'
    elif qtr.upper() == 'WINTER':
        qtr_num = '03'
    elif qtr.upper() == 'SPRING':
        qtr_num = '14'
    elif qtr.upper() == 'SUMMER1':
        qtr_num = '25'
    elif qtr.upper() == 'SUMMER2':
        qtr_num = '76'
    elif qtr.upper() == 'SUMMER10':
        qtr_num = '39'
    elif qtr.upper() == 'SUMMERCOM':
        qtr_num = '51'

    if not qtr_num:
        raise ValueError('INVALID QUARTER! qtr must be FALL, WINTER, SPRING, SUMMER1, SUMMER2, SUMMER10, or SUMMERCOM')

    form_data = {
        'YearTerm': f'{year}-{qtr_num}',
        'ShowComments': 'off',
        'ShowFinals': 'on',
        'Breadth': 'any',
        'Dept': dept,
        'CourseNum': course_num,
        'Division': 'ANY',
        'ClassType': 'ALL',
        'FullCourses': 'ANY',
        'FontSize': '100',
        'CancelledCourses': 'Exclude',
        'Submit': 'Display Text Results'
    }

    response = requests.post(BASE_URL, data=form_data)
    if response.status_code != 200:
        print('ERROR: RESPONSE CODE ' + str(response.status_code) + ' FROM WEBSOC POST')
        return

    data = response.text
    response.close()

    final_string = ''
    start_line = None

    for line in data.splitlines():
        if start_line:
            if line == '':
                break
            if '~' not in line and 'OPEN' in line:
                final_string += line + '\n'
        else:
            if line.strip().startswith('CCode'):
                start_line = {
                    'course_code': (line.index('CCode'), line.index('Typ')),
                    'type': (line.index('Typ'), line.index('Sec')),
                    'time': (line.index('Time'), line.index('Place')),
                    'final': (line.index('Final'), line.index('Max')),
                    'status': (line.index('Status'), len(line)),
                    'section': (line.index('Sec'), line.index('Unt'))
                }

    if not start_line:
        return

    return final_string.rstrip('\n'), start_line


def get_data(classes: list) -> dict:
    final_dict = defaultdict(dict)
    for dept, course_num, year, qtr in classes:
        data, indexes = make_request(dept, course_num, year, qtr)
        print(indexes)
        for line in data.splitlines():
            name = dept + ' ' + course_num
            code_s, code_e = indexes['course_code']
            type_s, type_e = indexes['type']
            time_s, time_e = indexes['time']
            final_s, final_e = indexes['final']
            status_s, status_e = indexes['status']
            section_s, section_e = indexes['section']

            final_dict[name][line[code_s:code_e]] = {
                'type': line[type_s:type_e].rstrip(' '),
                'time': line[time_s:time_e].rstrip(' '),
                'final': line[final_s:final_e].rstrip(' '),
                'status': line[status_s:status_e].rstrip(' '),
                'section': line[section_s:section_e].rstrip(' ')
            }

    return dict(final_dict)


if __name__ == '__main__':
    d = input('Enter department: ')
    n = input('Enter course number: ')
    y = input('Enter year: ')
    q = input('Enter quarter: ')

    d2 = input('Enter department: ')
    n2 = input('Enter course number: ')
    y2 = input('Enter year: ')
    q2 = input('Enter quarter: ')
    print(get_data([(d, n, y, q), (d2, n2, y2, q2)]))

    # d = 'I&C SCI'
    # n = '32A'
    # y = '2020'
    # q = 'FALL'
    # first = make_request(d, n, y, q)
    # n = '6B'
    # second = make_request(d, n, y, q)
    # print(first.splitlines()[0])
    # print(second.splitlines()[0])
