import pandas as pd
from openpyxl import Workbook

from . import util
from .client import Client
from .employee import Employee


def read(file):
    data = pd.read_excel(file, sheet_name=0, usecols=[
        'Date', 'Work', 'Client', 'Team Member', 'Role', 'Task Type', 'Time (Minutes)'])
    employees = {}
    clients = {}
    roles = {}
    for index, row in data.iterrows():
        if row['Team Member'] != 'New Client Queue -1':

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


def run(file, start_date, end_date):
    clients, roles, employees = read(file)

    wb = util.write_workbook(clients, roles, employees,
                             start_date, end_date)
    return(wb)
