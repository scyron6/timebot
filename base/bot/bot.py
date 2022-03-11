import pandas as pd
from openpyxl import Workbook
import math

from . import util
from .client import Client
from .employee import Employee
from base.models import Work


def read(file, clients, roles, employees, user, timesheet):
    data = pd.read_excel(file, sheet_name=0, usecols=[
        'Date', 'Work', 'Client', 'Team Member', 'Role', 'Task Type', 'Time (Minutes)'])
    for index, row in data.iterrows():
        if row['Team Member'] != 'New Client Queue -1':
            work_label = ""
            if isinstance(row['Work'], float):
                work_label = "Unlabeled Work"
            else:
                work_label = row['Work']
            Work.objects.create(timesheet=timesheet, user=user, employee=row["Team Member"], client=row["Client"], minutes=row["Time (Minutes)"], date=row["Date"], work=work_label,role=row["Role"], task=row['Task Type'] )

            if row['Client'] in clients:
                clients[row['Client']].add_minutes(
                    row['Time (Minutes)'])
            else:
                clients[row['Client']] = Client(row['Time (Minutes)'])

            clients[row['Client']].add_minutes_to_work(
                row['Work'], row['Time (Minutes)'])

            if row['Role'] in roles:
                roles[row['Role']] += row['Time (Minutes)']
            else:
                roles[row['Role']] = row['Time (Minutes)']

            if row['Team Member'] not in employees:
                employees[row['Team Member']] = Employee()

            employees[row['Team Member']].add_hours_to_client(
                row['Client'], row['Time (Minutes)'])
            employees[row['Team Member']].add_hours_to_task(
                row['Task Type'], row['Time (Minutes)'])
            employees[row['Team Member']].add_hours_to_role(
                row['Role'], row['Time (Minutes)'])
            employees[row['Team Member']].add_work_to_client(
                row['Client'], row['Work'], row['Time (Minutes)'])

    return clients, roles, employees


def run(files, start_date, end_date, user, timesheet):
    clients = {}
    roles = {}
    employees = {}
    for file in files:
        read(file, clients, roles, employees, user, timesheet)

    wb = util.write_workbook(clients, roles, employees,
                             start_date, end_date)
    return(wb)
