from schedule_api import find_teacher_rating
import re

# For TimeComparison class
TIME_RE = re.compile(
    r'^((?P<mon>M)|(?P<tue>Tu)|(?P<wed>W)|(?P<thu>Th)|(?P<fri>F))+ +(?P<hstart>\d?\d):(?P<mstart>\d\d)- *(?P<hend>\d?\d):(?P<mend>\d\d)(?P<pm>p)?$')
FINAL_RE = re.compile(r'^(?P<day>.+)(?P<hstart>\d?\d):(?P<mstart>\d\d)- *(?P<hend>\d?\d):(?P<mend>\d\d)(?P<pm>pm)$')

# also someone needs needs to create fake api function in schedule api

# Class is helpful for is_valid_time
class TimeComparison:
    def __init__(self, time_str):
        match = re.match(TIME_RE, time_str)
        if match:
            self.days = set()
            if match.group('mon'):
                self.days.add('M')
            if match.group('tue'):
                self.days.add('Tu')
            if match.group('wed'):
                self.days.add('W')
            if match.group('thu'):
                self.days.add('Th')
            if match.group('fri'):
                self.days.add('F')
        if not match:
            match = re.match(FINAL_RE, time_str)
            self.days = {match.group('day')}

        self.start_time = (int(match.group('hstart')), int(match.group('mstart')))
        self.end_time = (int(match.group('hend')), int(match.group('mend')))

        if match.group('pm') and self.end_time[0] != 12:
            self.end_time = self.end_time[0] + 12, self.end_time[1]
        if abs(self.end_time[0] - self.start_time[0]) > 4:
            self.start_time = self.start_time[0] + 12, self.start_time[1]

    def conflicts_with(self, other: 'TimeComparison') -> bool:
        same_days = False
        for day in self.days:
            if day in other.days:
                same_days = True

        if not same_days:
            return False

        starts_after_other_ends = False
        ends_before_other_starts = False

        if self.start_time[0] > other.end_time[0]:
            starts_after_other_ends = True
        elif self.start_time[0] == other.end_time[0] and self.start_time[1] >= other.end_time[1]:
            starts_after_other_ends = True

        if self.end_time[0] < other.start_time[0]:
            ends_before_other_starts = True
        elif self.end_time[0] == other.start_time[0] and self.end_time[1] <= other.start_time[1]:
            ends_before_other_starts = True

        return not (starts_after_other_ends or ends_before_other_starts)


def generate_all_classes(classes: list) -> list:
    # recursive, generate list of all possible schedules - no matter valid or not
    pass


# lmk what you think, but this should just be a dict, not a list, if we're sorting by
# course code v
# {course_code:{instructor: str, type: str, time: str, final: str, status: str, section: str}, ...}

# Tested somewhat, this seems to work!!!
def is_valid_time(classes: dict) -> bool:
    # jakub
    '''
    checks if the classes (time, finals) are conflicting
    '''
    # TuTh  6:30- 7:50p

    for class1 in classes.values():
        if class1['final'] == '' or class1['time'] == '*TBA*':
            continue
        class1_time = TimeComparison(class1['time'])
        class1_final = TimeComparison(class1['final'])
        for class2 in classes.values():
            if class1 is class2 or class2['final'] == '' or class2['time'] == '*TBA*':
                continue
            class2_time = TimeComparison(class2['time'])
            class2_final = TimeComparison(class2['final'])
            if class1_time.conflicts_with(class2_time) or class1_final.conflicts_with(class2_final):
                return False

    return True


def rate_prof(classes: list) -> int:
    # rates based on professor rating, higher rating = good
    # nathan
    pass


def rate_time(classes: list, pref_time: int) -> int:
    # rates based on distance from time; bigger distance = higher rating, higher rating = bad
    return abs(CLASS_TIME - pref_time)


if __name__ == '__main__':
    # file = open('courses.json')
    # data = json.load(file)
    test_dict = [{'I&C SCI 33': {'instructor': 'Patty', "type": "code", "time": '1:00pm', "final": "1:00pm 1/20/12",
                                 'status': 'Full', 'section': '2A'}}]