import pandas as pd
import gurobipy as gp
from gurobipy import GRB


def assign(excel_path):
    m = gp.Model()

    print('assign_task_started')
    print(type(excel_path))
    print('asda')
    excel_file = pd.ExcelFile(excel_path)

    print('parsing')
    # parsing
    df_courses = excel_file.parse('COURSES', usecols='A,C')
    df_c = excel_file.parse('COURSES')
    df_pre = excel_file.parse('PREASSIGNMENTS', index_col=0)
    df_users = excel_file.parse('USERS')
    df_sch = excel_file.parse('EXAM_SCHEDULE')
    df_inv = excel_file.parse('INVIGILATORS')

    # sets
    print('sets')
    invigilators = list(df_inv.loc[:, 'invigilatorid'])
    exams = list(df_sch.loc[:, 'examid'])
    time_slots = [f't{i + 1}' for i in range(len(days) * len(hours))]

    u = {}

    V = {
        (6, '113'),
        (7, '106'),
    }

    # parameters
    print('param')
    req_inv = list(df_sch.loc[:, 'requiredInv'])
    req = dict(zip(exams, req_inv))

    exam_weights = list(df_sch.loc[:, 'Eweight'])
    weight = dict(zip(exams, exam_weights))

    exam_date = list(df_sch.loc[:, 'Edate'])
    exam_time_slot = list(df_sch.loc[:, 'EtimeSlot'])
    time = list(zip(exam_time_slot, exam_date))
    time = [list(a) for a in time]

    hours = list(set(exam_time_slot))
    hours.sort()

    days = list(set(exam_date))
    days.sort()

    for i in time:
        i[0] = hours.index(i[0]) + 1

    for i in time:
        i[1] = days.index(i[1]) + 1

    time2 = [time_slots[i[0] + (i[1] - 1)*4 - 1] for i in time]

    time3 = list(zip(exams, time2))

    time4 = {exams[a]: time2[a] for a in range(31)}

    def check(j, t):
        return time4[j] == t

    not_avail = {}

    pre_assign = {
        (6, '113'): 1,
        (7, '106'): 1,
    }

    cost = {b: 1 for b in time3}

    load_ratio = list(df_inv.loc[:, 'loadRatio'])
    load = dict(zip(invigilators, load_ratio))

    # decision variables
    print('decision variables')
    y = m.addVars(invigilators, exams, vtype=gp.GRB.BINARY, name="y")

    r1 = m.addVar(lb=0.0, name="r1")
    r2 = m.addVar(lb=0.0, name="r2")

    # Constraints
    print('const')
    # C1
    m.addConstrs((gp.quicksum(check(j, t) * y[i, j] for j in exams) <= 1
                  for t in time_slots
                  for i in invigilators
                  ), name='c1')
    m.update()

    # C2
    m.addConstrs((gp.quicksum(y[i, j] for i in invigilators) == req[j]
                  for j in exams), 'c2')
    m.update()

    # C3
    # m.addConstrs((y[i,j] == pre_assign[i,j] for i,j in V), 'c3')

    # C4
    m.addConstrs((gp.quicksum(y[i, j] * check(j, t) for j in exams) == - 1
                  for i, t in u), 'c4')
    m.update()

    # C5
    m.addConstrs((gp.quicksum(y[i, j] * weight[j] for j in exams) <= load[i]*r1
                  for i in invigilators
                  for t in time_slots), 'c5')
    m.update()

    # C6
    m.addConstrs((gp.quicksum(y[i, j] * check(j, t) for j in exams) <= r2
                  for i in invigilators
                  for t in time_slots), 'c6')
    m.update()

    # Objective
    print('obj')
    obj = gp.quicksum(y[i, j] * check(j, t)
                      for i in invigilators
                      for j in exams
                      for t in time_slots) + r1 + r2

    m.setObjective(obj, GRB.MINIMIZE)

    m.optimize()

    h = {}
    a = []
    for i in invigilators:
        for j in exams:
            a.append(int(y[i, j].x))
        h.update({i: a})
        a = []
    yy = pd.DataFrame.from_dict(h, orient='index', columns=[j for j in exams])

    print('done')

    yy.to_excel('assignments.xlsx')
