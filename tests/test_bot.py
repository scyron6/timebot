from base.bot import bot


# Tests with 1 Team Member File
def test_run_one_team_member():
    file_path = "/Users/stephencyron/Coding/Saas/timebot/tests/Karbon Timesheets - Tom Brady Tests.xlsx"
    clients = {}
    roles = {}
    employees = {}

    bot.read(file_path, clients, roles, employees)

    assert len(employees) == 1
    assert employees['Tom Brady'].minutes_per_client['Flag Football Team'] == 210
    assert employees['Tom Brady'].minutes_per_client['Tampa Bay Buccaneers'] == 300

    assert employees['Tom Brady'].minutes_per_role['Coach'] == 210
    assert employees['Tom Brady'].minutes_per_role['QB'] == 300

    assert employees['Tom Brady'].minutes_per_task['Coaching'] == 210
    assert employees['Tom Brady'].minutes_per_task['Playing'] == 300

    assert len(employees['Tom Brady'].work_per_client) == 2
    assert len(
        employees['Tom Brady'].work_per_client['Flag Football Team']) == 3
    assert employees['Tom Brady'].work_per_client['Flag Football Team']['Team Meeting'] == 30
    assert employees['Tom Brady'].work_per_client['Flag Football Team']['Practice'] == 60
    assert employees['Tom Brady'].work_per_client['Flag Football Team']['Game'] == 120

    assert len(
        employees['Tom Brady'].work_per_client['Tampa Bay Buccaneers']) == 4
    assert employees['Tom Brady'].work_per_client['Tampa Bay Buccaneers']['Contract Talks'] == 30
    assert employees['Tom Brady'].work_per_client['Tampa Bay Buccaneers']['Retirement Ceremony'] == 60
    assert employees['Tom Brady'].work_per_client['Tampa Bay Buccaneers']['Game'] == 120
    assert employees['Tom Brady'].work_per_client['Tampa Bay Buccaneers']['Practice'] == 90

    assert len(roles) == 2
    assert roles['Coach'] == 210
    assert roles['QB'] == 300

    assert len(clients) == 2
    assert clients['Flag Football Team'].total_minutes == 210
    assert clients['Tampa Bay Buccaneers'].total_minutes == 300

    assert len(clients['Flag Football Team'].minutes_per_work) == 3
    assert clients['Flag Football Team'].minutes_per_work['Team Meeting'] == 30
    assert clients['Flag Football Team'].minutes_per_work['Practice'] == 60
    assert clients['Flag Football Team'].minutes_per_work['Game'] == 120

    assert len(clients['Tampa Bay Buccaneers'].minutes_per_work) == 4
    assert clients['Tampa Bay Buccaneers'].minutes_per_work['Contract Talks'] == 30
    assert clients['Tampa Bay Buccaneers'].minutes_per_work['Retirement Ceremony'] == 60
    assert clients['Tampa Bay Buccaneers'].minutes_per_work['Game'] == 120
    assert clients['Tampa Bay Buccaneers'].minutes_per_work['Practice'] == 90

# Tests with 2 Team Member File


def test_run_two_team_members():
    file_path = "/Users/stephencyron/Coding/Saas/timebot/tests/Karbon Timesheets - Tom Brady & Aaron Rodgers Tests.xlsx"
    clients = {}
    roles = {}
    employees = {}

    bot.read(file_path, clients, roles, employees)

    assert len(employees) == 2
    assert employees['Tom Brady'].minutes_per_client['Flag Football Team'] == 210
    assert employees['Tom Brady'].minutes_per_client['Tampa Bay Buccaneers'] == 300
    assert employees['Aaron Rodgers'].minutes_per_client['Flag Football Team'] == 210
    assert employees['Aaron Rodgers'].minutes_per_client['Green Bay Packers'] == 310

    assert employees['Tom Brady'].minutes_per_role['Coach'] == 210
    assert employees['Tom Brady'].minutes_per_role['QB'] == 300
    assert employees['Aaron Rodgers'].minutes_per_role['Assistant Coach'] == 210
    assert employees['Aaron Rodgers'].minutes_per_role['QB'] == 310

    assert employees['Tom Brady'].minutes_per_task['Coaching'] == 210
    assert employees['Tom Brady'].minutes_per_task['Playing'] == 300
    assert employees['Aaron Rodgers'].minutes_per_task['Coaching'] == 210
    assert employees['Aaron Rodgers'].minutes_per_task['Playing'] == 310

    assert len(employees['Tom Brady'].work_per_client) == 2
    assert len(
        employees['Tom Brady'].work_per_client['Flag Football Team']) == 3
    assert employees['Tom Brady'].work_per_client['Flag Football Team']['Team Meeting'] == 30
    assert employees['Tom Brady'].work_per_client['Flag Football Team']['Practice'] == 60
    assert employees['Tom Brady'].work_per_client['Flag Football Team']['Game'] == 120

    assert len(employees['Aaron Rodgers'].work_per_client) == 2
    assert len(
        employees['Aaron Rodgers'].work_per_client['Flag Football Team']) == 3
    assert employees['Aaron Rodgers'].work_per_client['Flag Football Team']['Team Meeting'] == 30
    assert employees['Aaron Rodgers'].work_per_client['Flag Football Team']['Practice'] == 60
    assert employees['Aaron Rodgers'].work_per_client['Flag Football Team']['Game'] == 120

    assert len(
        employees['Aaron Rodgers'].work_per_client['Green Bay Packers']) == 4
    assert employees['Aaron Rodgers'].work_per_client['Green Bay Packers']['Contract Talks'] == 40
    assert employees['Aaron Rodgers'].work_per_client['Green Bay Packers']['Team Photos'] == 30
    assert employees['Aaron Rodgers'].work_per_client['Green Bay Packers']['Game'] == 120
    assert employees['Aaron Rodgers'].work_per_client['Green Bay Packers']['Practice'] == 120

    assert len(roles) == 3
    assert roles['Coach'] == 210
    assert roles['Assistant Coach'] == 210
    assert roles['QB'] == 610

    assert len(clients) == 3
    assert clients['Flag Football Team'].total_minutes == 420
    assert clients['Tampa Bay Buccaneers'].total_minutes == 300
    assert clients['Green Bay Packers'].total_minutes == 310

    assert len(clients['Flag Football Team'].minutes_per_work) == 3
    assert clients['Flag Football Team'].minutes_per_work['Team Meeting'] == 60
    assert clients['Flag Football Team'].minutes_per_work['Practice'] == 120
    assert clients['Flag Football Team'].minutes_per_work['Game'] == 240

    assert len(clients['Tampa Bay Buccaneers'].minutes_per_work) == 4
    assert clients['Tampa Bay Buccaneers'].minutes_per_work['Contract Talks'] == 30
    assert clients['Tampa Bay Buccaneers'].minutes_per_work['Retirement Ceremony'] == 60
    assert clients['Tampa Bay Buccaneers'].minutes_per_work['Game'] == 120
    assert clients['Tampa Bay Buccaneers'].minutes_per_work['Practice'] == 90

    assert len(clients['Green Bay Packers'].minutes_per_work) == 4
    assert clients['Green Bay Packers'].minutes_per_work['Contract Talks'] == 40
    assert clients['Green Bay Packers'].minutes_per_work['Team Photos'] == 30
    assert clients['Green Bay Packers'].minutes_per_work['Game'] == 120
    assert clients['Green Bay Packers'].minutes_per_work['Practice'] == 120


def test_inputing_both_files():
    file = "/Users/stephencyron/Coding/Saas/timebot/tests/Karbon Timesheets - Tom Brady & Aaron Rodgers Tests.xlsx"
    file2 = "/Users/stephencyron/Coding/Saas/timebot/tests/Karbon Timesheets - Tom Brady Tests.xlsx"
    clients = {}
    roles = {}
    employees = {}

    bot.read(file, clients, roles, employees)
    bot.read(file2, clients, roles, employees)

    assert len(roles) == 3
    assert roles['Coach'] == 420
    assert roles['Assistant Coach'] == 210
    assert roles['QB'] == 910