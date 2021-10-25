import json
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
import numpy as np
import geatpy as ea
import matplotlib.pyplot as plt
import time
import datetime



# def DateInput(str):
#     date = str.split('-')
#     for i in range(3):
#         date[i] = int(date[i])
#     someday = datetime.date(year=date[0],month=date[1],day=date[2])
#     return someday
#
# schedule = content['schedule']
# day1 = DateInput(schedule['startTermBegin'])
# day2 = DateInput(schedule['startTermEnd'])
# interval = day2 - day1
# print(interval.days)
#
# schedule = content['schedule']
# day1 = schedule['startTermBegin']
# day2 = schedule['startTermEnd']
#
# day1 = datetime.datetime.strptime(day1,'%Y-%m-%d')
# day2 = datetime.datetime.strptime(day2,'%Y-%m-%d')
# interval = day2 - day1
# print(interval.days)

class generation():
    with open('排课入参测试数据.json', 'rb') as f:
        content = json.load(f)
    students = content['students']
    teachers = content['teachers']
    classroom = content['classrooms']
    subject = content['subject']
    courses = content['courses']
    tools = content['tools']
    schedule = content['schedule']

    def __init__(self):
        return

    def course_count(self):
        self.course_num = len(generation.courses)
        return self.course_num

    def course_teacher_relation(self):
        dict = {}
        for course in generation.courses:
            dict[course['code']] = list()
        for t in generation.teachers:
            for c in t['courseCode']:
                dict[c].append(t['idNo'])
        self.course_teacher_dict = dict
        return dict

    def course_room_relation(self):
        dict = {}
        for course in generation.courses:
            dict[course['code']] = course['classroomCode']
        self.course_room_dict = dict
        return dict

# 根据校历计算课时数
    def schedule_info_read(self):
        week_mask = str()
        week_on = np.array(7)
        week_on[0] = int(generation.schedule["monday"])
        week_on[1] = int(generation.schedule["tuesday"])
        week_on[2] = int(generation.schedule["wednesday"])
        week_on[3] = int(generation.schedule["thursday"])
        week_on[4] = int(generation.schedule["friday"])
        week_on[5] = int(generation.schedule["saturday"])
        week_on[6] = int(generation.schedule["sunday"])
        lessonNumAm = int(generation.schedule["lessonNumAm"])
        lessonNumPm = int(generation.schedule["lessonNumPm"])
        if week_on[0] != 0:
            week_mask += "Mon"
        if week_on[1] != 0:
            week_mask += " Tue"
        if week_on[2] != 0:
            week_mask += " Wed"
        if week_on[3] != 0:
            week_mask += " Thu"
        if week_on[4] != 0:
            week_mask += " Fri"
        if week_on[5] != 0:
            week_mask += " Sat"
        if week_on[6] != 0:
            week_mask += " Sun"

        holiday_list = CustomBusinessDay(holidays=generation.schedule["holiday"], weekmask = week_mask)
        s_day = self.schedule["startTermBegin"]
        e_day = self.schedule["startTermEnd"]
        bus_day = pd.date_range(start=s_day, end=e_day, freq='b')

        # length = len(bus_day)
        # extra_work_day = ['2021-10-09']
        # extra_len = 0
        # for i in extra_work_day:
        #     if s_day <= i <= e_day:
        #         extra_len = extra_len + 1

        # work_data = length + extra_len
        self.bus_day = bus_day

        day_period = list()
        count = 0
        period_sum = 0
        for day in bus_day:
            weekday = day.weekday() + 1
            period = am_times[2 * weekday] * am_times[2 * weekday + 1] \
                     + pm_times[2 * weekday] * pm_times[2 * weekday + 1]
            day_period.append(period)
            count += 1
            period_sum += period
        self.period_sum = period_sum
        self.day_period = day_period
        return bus_day

# 科目信息读取,在教师信息之前读入
    def subject_info(self):
        subject_num = len(generation.subject)
        sub_tea_relation = dict()
        for subject in generation.subject:
            sub_tea_relation[subject['code']] = list()
        self.sub_tea_relation = sub_tea_relation
        return
# 老师信息读取和安排
    def teacher_info(self):
        teacher_num = len(generation.teachers)
        teacher_work = dict()
        for i in generation.teachers:
            for j in i["courseCode"]:
                self.sub_tea_relation[j].append(i["idNo"])
            teacher_work[i["idNo"]] = 0
        self.teacher_work = teacher_work
        return

# 课程信息读取和安排
    def course_info(self):

        return


 # 一周内每天的课程情况安排
    def weekly_times(self):
        days = 5
        am_times = [3, 1] * days
        pm_times = [2, 1] * days
        dayly_times = [0] * days
        for i in range(days):
            dayly_times[i] = am_times[2*i] * am_times[2*i + 1] + pm_times[2*i] * pm_times[2*i + 1]
        dayly_times = np.array(dayly_times)
        weekly_times = dayly_times.sum()
        self.dayly_times = dayly_times
        self.weekly_times = weekly_times
        return weekly_times


    def arrange_plan_generation(self):
        generation.teacher_count(self)

        generation.course_teacher_relation(self)
        arrange_dict = dict()
        count = 0
        for course in self.courses:
            course_code = int(course['code']) % 10 - 1
            course_code = course_code * 3
            if len(self.course_teacher_dict[course['code']]) == 1:
                t = 3
                for i in range(3):
                    teacher = self.course_teacher_dict[course['code']][0]
                    teacher_code = int(teacher) % 10 - 1
                    arrange_dict[count] = {'course_num': course_code + i,
                                           'teacher_num': teacher_code,
                                           'weekly_course': t}
                    count += 1
                    t -= 1
            else:
                t = 3
                teacher1 = self.course_teacher_dict[course['code']][0]
                teacher_code = int(teacher1) % 10 - 1
                arrange_dict[count] = {'course_num': course_code,
                                       'teacher_num': teacher_code,
                                       'weekly_course': t}
                count += 1
                t -= 1

                teacher2 = self.course_teacher_dict[course['code']][1]
                teacher_code = int(teacher2) % 10 - 1
                arrange_dict[count] = {'course_num': course_code + 1,
                                       'teacher_num': teacher_code,
                                       'weekly_course': t}
                count += 1
                t -= 1

                arrange_dict[count] = {'course_num': course_code + 2,
                                       'teacher_num': teacher_code,
                                       'weekly_course': t}
                count += 1

        self.arrange_dict = arrange_dict
        return arrange_dict

plan = generation()
work_data, week_num = plan.schedule_info_read()
print(work_data, week_num)