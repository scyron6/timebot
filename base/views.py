from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.db.models import Sum

from datetime import date, datetime
from openpyxl.writer.excel import save_virtual_workbook
from .bot import bot
from .models import Work, Timesheet


def index(request):
    return render(request, 'base/index.html')


@login_required(login_url='login')
def dashboard(request):

    labels = []
    data = []
    getSessionDates(request)
    
    total_clients = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('client').distinct().count()
    total_minutes = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).aggregate(Sum('minutes'))
    total_employees = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('employee').distinct().count()
    total_roles = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('role').distinct().count()
    time_by_client = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('client').annotate(total_time=Sum('minutes')).order_by('-total_time')
    work_entries_by_client = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('client').annotate(total_time=Sum('minutes')).order_by('-total_time')[:5]
    work_entries_by_employee = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('employee').order_by('employee').annotate(total_time=Sum('minutes'))
    work_entries_by_role = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('role').annotate(total_time=Sum('minutes')).order_by('-total_time')[:5]
    work_entries_by_task = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('task').annotate(total_time=Sum('minutes')).order_by('-total_time')[:5]
    
    for entry in time_by_client:
        labels.append(entry['client'])
        data.append(entry['total_time'])
    

    context = {
        'total_clients': total_clients,
        'total_minutes': total_minutes,
        'total_employees': total_employees,
        'total_roles': total_roles,
        'work_entries_by_client': work_entries_by_client,
        'work_entries_by_employee': work_entries_by_employee,
        'work_entries_by_role': work_entries_by_role,
        'work_entries_by_task': work_entries_by_task,
        'time_by_client': time_by_client,
        'start_date': request.session['start_date'],
        'end_date': request.session['end_date'],
        'sidebar_select': '#dashboard_nav'
    }
    return render(request, 'base/dashboard.html', context)


@login_required(login_url='login')
def clients(request):
    getSessionDates(request)
    work_entries_by_client = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('client').annotate(total_time=Sum('minutes')).order_by('client')
    context = {
        'work_entries_by_client': work_entries_by_client,
        'start_date': request.session['start_date'],
        'end_date': request.session['end_date'],
        'sidebar_select': '#clients_nav'
    }
    return render(request, 'base/clients.html', context)

@login_required(login_url='login')
def client(request):
    client_name = ""
    if 'client_name' in request.GET:
        client_name = request.GET['client_name']
    getSessionDates(request)

    work_entries_for_client = Work.objects.filter(user=request.user).filter(client=client_name).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('client').values('employee', 'work', 'minutes', 'date').order_by('date')

    context = {
        'client_name': client_name,
        'work_entries_for_client': work_entries_for_client,
        'start_date': request.session['start_date'],
        'end_date': request.session['end_date'],
        'sidebar_select': '#clients_nav'
    }
    return render(request, 'base/client.html', context)


@login_required(login_url='login')
def employees(request):
    getSessionDates(request)
    work_entries_by_employee = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('employee').annotate(total_time=Sum('minutes')).order_by('employee')
    context = {
        'work_entries_by_employee': work_entries_by_employee,
        'start_date': request.session['start_date'],
        'end_date': request.session['end_date'],
        'sidebar_select': '#employees_nav'
    }
    return render(request, 'base/employees.html', context)

@login_required(login_url='login')
def employee(request):
    employee_name = ""
    if 'employee_name' in request.GET:
        employee_name = request.GET['employee_name']

    getSessionDates(request)

    time_by_client = Work.objects.filter(user=request.user).filter(employee=employee_name).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('client').annotate(total_time=Sum('minutes')).order_by('client')
    time_by_task = Work.objects.filter(user=request.user).filter(employee=employee_name).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('task').annotate(total_time=Sum('minutes')).order_by('task')
    time_by_role = Work.objects.filter(user=request.user).filter(employee=employee_name).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('role').annotate(total_time=Sum('minutes')).order_by('role')

    context = {
        'employee_name': employee_name,
        'time_by_client': time_by_client,
        'time_by_task': time_by_task,
        'time_by_role': time_by_role,
        'start_date': request.session['start_date'],
        'end_date': request.session['end_date'],
        'sidebar_select': '#employees_nav'
    }
    return render(request, 'base/employee.html', context)


@login_required(login_url='login')
def roles(request):
    getSessionDates(request)

    work_entries_by_role = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('role').annotate(total_time=Sum('minutes')).order_by('role')
    context = {
        'work_entries_by_role': work_entries_by_role,
        'start_date': request.session['start_date'],
        'end_date': request.session['end_date'],
        'sidebar_select': '#roles_nav'
    }
    return render(request, 'base/roles.html', context)

@login_required(login_url='login')
def role(request):
    role_name = ""
    if 'role_name' in request.GET:
        role_name = request.GET['role_name']
    
    getSessionDates(request)

    work_entries_for_role = Work.objects.filter(user=request.user).filter(role=role_name).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('employee').annotate(total_time=Sum('minutes'))

    context = {
        'role_name': role_name,
        'work_entries_for_role': work_entries_for_role,
        'start_date': request.session['start_date'],
        'end_date': request.session['end_date'],
        'sidebar_select': '#roles_nav'
    }
    return render(request, 'base/role.html', context)

@login_required(login_url='login')
def tasks(request):
    getSessionDates(request)

    work_entries_by_task = Work.objects.filter(user=request.user).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('task').annotate(total_time=Sum('minutes')).order_by('task')
    context = {
        'work_entries_by_task': work_entries_by_task,
        'start_date': request.session['start_date'],
        'end_date': request.session['end_date'],
        'sidebar_select': '#tasks_nav'
    }
    return render(request, 'base/tasks.html', context)

@login_required(login_url='login')
def task(request):
    task_name = ""
    if 'task_name' in request.GET:
        task_name = request.GET['task_name']
    
    getSessionDates(request)

    work_entries_for_task = Work.objects.filter(user=request.user).filter(task=task_name).filter(date__range=[request.session['start_date'],request.session['end_date']]).values('employee').annotate(total_time=Sum('minutes'))

    context = {
        'task_name': task_name,
        'work_entries_for_task': work_entries_for_task,
        'start_date': request.session['start_date'],
        'end_date': request.session['end_date'],
        'sidebar_select': '#tasks_nav'
    }
    return render(request, 'base/task.html', context)

@login_required(login_url='login')
def timesheets(request):
    if request.method == 'POST':
        files = request.FILES.getlist('excel_timesheets')
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        # download = False
        # if 'download' in request.POST:
        #     download = True
        
        file_name = ""
        for file in files:
            file_name += file.name + ','
        timesheet = Timesheet.objects.create(file_name = file_name, user=request.user, start_date=start_date, end_date=end_date, submission_date=date.today())
        wb = bot.run(files, start_date, end_date, request.user, timesheet)

        # if download:
        #     filename = 'attachment; filename="Timesheet Summary ' + \
        #         start_date + ' - ' + end_date + '.xls"'
        #     response = HttpResponse(save_virtual_workbook(
        #         wb), headers={
        #             'Content_Type': 'application/vnd.ms-excel',
        #             'Content-Disposition': filename,
        #     })

        #     return response
        # else:
        return redirect('timesheets')

    timesheets = Timesheet.objects.filter(user=request.user).values('file_name', 'start_date', 'end_date', 'submission_date', 'pk').order_by('start_date')
    context = {
        'timesheets': timesheets,
        'sidebar_select': '#timesheets_nav'
    }
    return render(request, 'base/timesheets.html', context)

@login_required(login_url='login')
def timesheet(request, pk):
    timesheet = Timesheet.objects.get(pk=pk)

    if (request.user != timesheet.user):
        return HttpResponse("You aren't allowed here")

    timesheet_entries = Work.objects.filter(user=request.user).filter(timesheet=pk).values('date', 'work', 'client', 'employee', 'role', 'task', 'minutes')
    context = {
        'timesheet_pk': timesheet.pk,
        'timesheet_filename': timesheet.file_name,
        'timesheet_start_date': timesheet.start_date,
        'timesheet_end_date': timesheet.end_date,
        'timesheet_entries': timesheet_entries,
        'sidebar_select': '#timesheets_nav'
    }
    return render(request, 'base/timesheet.html', context)

@login_required(login_url='login')
def delete_timesheet(request, pk):
    timesheet = Timesheet.objects.get(pk=pk)

    if (request.user != timesheet.user):
        return HttpResponse("You aren't allowed here")
    
    if request.method == 'POST':
        timesheet.delete()
        return redirect('timesheets')

    return render(request, 'base/delete_timesheet.html')

@login_required(login_url='login')
def my_profile(request):
    context = {
        'sidebar_select': '#profile_nav'
    }
    return render(request, 'base/my_profile.html', context)

@login_required(login_url='login')
def tutorial(request):
    context = {
        'sidebar_select': '#tutorial_nav'
    }
    return render(request, 'base/tutorial.html', context)

def registerPage(request):
    if request.method == 'POST':
        # Get form values
        email = request.POST['email']
        username = email
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(
                        username=username, password=password, email=email)
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')
                    user.save()
                    login(request, user)
                    return redirect('my_profile')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'base/register.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=email)
        except:
            messages.error(request, 'User does not exist')

        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'base/login.html')


def logoutUser(request):
    logout(request)
    return redirect('index')

def getSessionDates(request):
    if not request.session.get('start_date'):
        request.session['start_date'] = datetime.strftime(date.today().replace(day=1), "%Y-%m-%d")

    if not request.session.get('end_date'):
        request.session['end_date'] = datetime.strftime(date.today(), "%Y-%m-%d")

    if 'start_date' in request.GET:
        request.session['start_date'] = request.GET['start_date']
    
    if 'end_date' in request.GET:
        request.session['end_date'] = request.GET['end_date']
