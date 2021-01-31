#testing out flask
#no hate name plz is beautiful

from flask import Flask, request,render_template
import os
import urllib
import random
import re
from time_compare import TimeComparison
from logic import get_optimal_time
from websoc_data import get_data
from datetime import datetime
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')
app = Flask(__name__, template_folder=template_path)
message = dict()
gen_courses = []
c_input = []
times_list = []
table_dict = dict()
time_increments = ['7:00 AM', '8:00 AM','9:00 AM','10:00 AM','11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM','4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM','8:00 PM', '9:00 PM'  ]
colors = ['color1','color2','color3','color4','color5','color6','color7','color8']

#['#DFFF00','#FFBF00','#FF7F50','#DE3163','#9FE2BF','#40E0D0','#6495ED','#CCCCFF']
#time_increments= enumerate(time_increments)
#gen_courses = [{'35570 ': {'name': 'I&C SCI 33', 'type': 'LEC', 'time': 'MWF   1:00- 1:50p', 'final': 'Wed, Mar 17, 1:30-3:30pm', 'status': 'OPEN', 'section': 'A', 'instructor': 'PATTIS, R.'}, '35581 ': {'name': 'I&C SCI 33', 'type': 'LAB', 'time': 'TuTh  2:00- 3:50p', 'final': '', 'status': 'OPEN', 'section': '1', 'instructor': 'CHIO, A.'}, '35600 ': {'name': 'I&C SCI 45', 'type': 'LEC', 'time': 'TuTh  5:00- 6:20p', 'final': 'Thu, Mar 18, 4:00-6:00pm', 'status': 'OPEN', 'section': 'A', 'instructor': 'IBRAHIM, M.'}, '33303 ': {'name': 'WRITING 39C', 'type': 'SEM', 'time': 'TBA', 'final': '', 'status': 'OPEN', 'section': 'C', 'instructor': 'VENEGAS, Y.'}}, 3.8]

@app.route('/', methods=['post', 'get'])
def getform():
    if request.method == 'POST':
        if "form" in request.form:
            if request.form["form"] == "const":
                quarter = request.form.get('quarter')  # access the data inside 
                year = request.form.get('year')
                time = request.form.get('time')
                message['quarter'] = quarter
                message['year'] = year
                message['time'] = time
            elif request.form["form"] == "speccourse":
                department = request.form.get('department')
                cnumber = request.form.get('course-number')
                if 'courses' in message:
                    if (cnumber,department) not in message['courses']:
                        message['courses'].append((cnumber,department))
                else:
                    message['courses'] = [(cnumber,department)]
        elif 'course_rem' in request.form and 'courses' in message:
            del message['courses'][int(request.form['course_rem'])]
        elif 'course_gen' in request.form and 'courses' in message and len(message['courses']) > 0 and 'quarter' in message and 'year' in message and 'time' in message:
            make_courses()
            make_table()
    return render_template('index.html', message=message,gen_courses=gen_courses,c_input = c_input, time_increments = time_increments, table_dict = table_dict)


def format_time(classes: dict) -> [(str, set, int, int)]:
    list_to_return = []
    for v,c in classes.items():
        if c['time'] == '*TBA*':
            continue
        c_time = TimeComparison(c['time'])
        start_hour, start_minute = c_time.start_time
        end_hour, end_minute = c_time.end_time
        start_hour -= 7
        end_hour -= 7

        start_tot_mins = start_minute + 60 * start_hour
        end_tot_mins = end_minute + 60 * end_hour
        list_to_return.append( (v, c_time.days, start_tot_mins, end_tot_mins) )
    return list_to_return


def make_courses():
    temp_colors = colors.copy()
    global c_input,gen_courses,times_list
    c_input = []
    gen_courses = []
    for course in message['courses']:
        c_input.append((course[1],course[0],message['year'],message['quarter']))
    courses = get_data(c_input)
    if message['time'] == 'Morning':
        pref_time = ('7:00','11:00')
    elif message['time'] == 'Noon':
        pref_time = ('11:00','14:00')
    elif message['time'] == 'Afternoon':
        pref_time = ('14:00','19:00')
    gen_courses = get_optimal_time(courses,pref_time)
    for c in gen_courses[0].keys():
        if len(temp_colors) == 0:
            temp_colors = colors.copy()
        gen_courses[0][c]['color'] = temp_colors.pop(random.randrange(len(temp_colors)))
    times_list = format_time(gen_courses[0])

def make_table():
    global table_dict
    for interval in range(0,90):
        for course in times_list:
            if (interval*10  == course[2]):
                table_dict[interval] = course 






# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)