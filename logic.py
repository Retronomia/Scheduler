from schedule_api import find_teacher_rating
from time_compare import TimeComparison
import re
import copy
import app.websoc_data


# {name: {course_code:{instructor: str, type: str, time: str, final: str, status: str, section: str}, ...},...}

def separate_non_classes(classes: dict) -> None:
    iteration_list_first = list(classes.keys())
    for class_name in iteration_list_first:
        iteration_list_second = list(classes[class_name].keys())
        type_to_check = classes[class_name][iteration_list_second[0]]["type"]
        for course_code in iteration_list_second:
            type1 = classes[class_name][course_code]["type"]

            if type1 != type_to_check:
                if str(class_name + " " + type1) not in classes.keys():
                    classes[str(class_name + " " + type1)] = {course_code: classes[class_name][course_code]}
                else:
                    classes[str(class_name + " " + type1)][course_code] = classes[class_name][course_code]
                del classes[class_name][course_code]


def generate_all_classes(classes: dict, index: int, current_schedule: dict, valid_list) -> list:
    # recursive, generate list of all possible schedules - no matter valid or not
    result = {}
    if index == len(list(classes.keys())) and is_valid_time(current_schedule):
        valid_list.append(current_schedule)
        return
    current_class = sorted(list(classes.keys()))[index]
    # print(current_class, classes[current_class])
    for class_times in list(classes[current_class].items()):
        next_schedule = copy.deepcopy(current_schedule)
        next_schedule[class_times[0]] = copy.deepcopy(class_times[1])
        generate_all_classes(classes, index + 1, next_schedule, valid_list)


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


# {course_code:{instructor: str, type: str, time: str, final: str, status: str, section: str}, ...}
def rate_prof(classes: dict, cache: dict, class_limit: dict) -> int:
    # rates based on professor rating, higher rating = good

    for class1 in class_limit.values():
        if class1>5:
            return 0
    result = 0
    total_number = 0
    for class1 in classes.values():
        if class1["type"] == "LEC" or class1['type'] == "SEM":
            if "instructor" in class1.keys() and class1["instructor"] in cache.keys():
                result_temp = cache[class1["instructor"]]
            elif "instructor" in class1.keys():
                result_temp = find_teacher_rating(class1["instructor"])
                cache[class1["instructor"]] = result_temp
            if class1["name"] in class_limit.keys():
                class_limit[class1["name"]]+=1
            else:
                class_limit[class1["name"]]=1
            if result_temp != {}:
                if len(result_temp['rating']) > 1 and result_temp['rating'][1] != ".":
                    result_temp['rating'] = result_temp['rating'][0:1]
                try:
                    result += float(result_temp['rating'])
                    total_number += 1
                except:
                    pass
    if total_number == 0:
        return 0
    return result / total_number


def rate_time(classes: dict, pref_time: (str, str)) -> float:
    # pref_time input should be a tuple (10:30, 15:30) in 24hour time
    # rates based on distance from time; bigger distance = lower rating, higher rating = good
    total_score = 0
    for course in classes.values():
        if course['time'] == '*TBA*':
            continue
        pref_h_1, pref_m_1 = pref_time[0].split(':')
        pref_h_2, pref_m_2 = pref_time[1].split(':')

        pref_total_mins_1 = int(pref_m_1) + 60 * int(pref_h_1)
        pref_total_mins_2 = int(pref_m_2) + 60 * int(pref_h_2)
        pref_avg_mins = round((pref_total_mins_1 + pref_total_mins_2) / 2)

        class_time = TimeComparison(course['time'])

        course_start_mins = class_time.start_time[1] + 60 * class_time.start_time[0]
        course_end_mins = class_time.end_time[1] + 60 * class_time.end_time[0]
        course_avg_mins = round((course_start_mins + course_end_mins) / 2)

        total_score += abs(pref_avg_mins - course_avg_mins)

    return 5 - (total_score / 144)


def get_optimal_time(classes: dict, pref_time: (str, str)):
    # pref_time input should be a tuple (10:30, 15:30) in 24hour time
    separate_non_classes(classes)
    valid_list = []
    generate_all_classes(classes, 0, {}, valid_list)
    best_rating = -1
    current_optimal = {}
    avg_prof_rating = 0
    cache = {}
    class_limit = {}
    for valid_schedule in valid_list:

        prof_rate = rate_prof(valid_schedule, cache, class_limit)
        time_rate = rate_time(valid_schedule, pref_time)
        weighted_rating = 0.7 * prof_rate + 0.3 * time_rate
        if weighted_rating > best_rating:
            current_optimal = valid_schedule
            best_rating = weighted_rating
            avg_prof_rating = prof_rate
    return [current_optimal, avg_prof_rating]


if __name__ == '__main__':
    pref_time = ("10:30", "15:30")
    test_classes = [("WRITING", "39C", "2021", "WINTER"), ("I&C Sci", "33", "2021", "WINTER")]
    test_dict = websoc_data.get_data(test_classes)
    print("testdict", test_dict)

    results = get_optimal_time(test_dict, pref_time)
    print("optimal", results)