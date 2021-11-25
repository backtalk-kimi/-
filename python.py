#coding=UTF-8
import numpy as np
from genetic import *
from pandas import *
from generation import *
import os

path = 'result.json'
if os.path.exists(path):  # 如果文件存在
    os.remove(path)
else:
    print('no such file:',path)  # 则返回文件不存在

plan = generation()
schedules = plan.arrange()
#种群规模popsize，精英个体数elite，进化代数maxiter
ga = GeneticOptimize()
bestSchedule,successMark= ga.evolution(schedules=schedules, roomRange=5,slotnum=19,plan= plan)

schedule_result = result_disply(bestSchedule, plan, successMark)



