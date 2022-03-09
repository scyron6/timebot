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
    
    start_date = date.today().replace(day=1)
    end_date = date.today()
    if 'start_date' in request.GET:
        start_date = datetime.strptime(request.GET['start_date'], "%Y-%m-%d")
    
    if 'end_date' in request.GET:
        end_date = datetime.strptime(request.GET['end_date'], "%Y-%m-%d")
    
    total_clients = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).values('client').distinct().count()
    total_minutes = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).aggregate(Sum('minutes'))
    total_employees = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).values('employee').distinct().count()
    total_roles = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).values('role').distinct().count()
    work_entries_by_client = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).values('client').annotate(total_time=Sum('minutes')).order_by('-total_time')[:5]
    work_entries_by_employee = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).values('employee').order_by('employee').annotate(total_time=Sum('minutes'))
    work_entries_by_role = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).values('role').annotate(total_time=Sum('minutes')).order_by('-total_time')[:5]
    context = {
        'total_clients': total_clients,
        'total_minutes': total_minutes,
        'total_employees': total_employees,
        'total_roles': total_roles,
        'work_entries_by_client': work_entries_by_client,
        'work_entries_by_employee': work_entries_by_employee,
        'work_entries_by_role': work_entries_by_role,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    return render(request, 'base/dashboard.html', context)


@login_required(login_url='login')
def clients(request):
    start_date = date.today().replace(day=1)
    end_date = date.today()
    if 'start_date' in request.GET:
        start_date = datetime.strptime(request.GET['start_date'], "%Y-%m-%d")
    
    if 'end_date' in request.GET:
        end_date = datetime.strptime(request.GET['end_date'], "%Y-%m-%d")
    work_entries_by_client = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).values('client').annotate(total_time=Sum('minutes')).order_by('client')
    context = {
        'work_entries_by_client': work_entries_by_client,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    return render(request, 'base/clients.html', context)


@login_required(login_url='login')
def employees(request):
    start_date = date.today().replace(day=1)
    end_date = date.today()
    if 'start_date' in request.GET:
        start_date = datetime.strptime(request.GET['start_date'], "%Y-%m-%d")
    
    if 'end_date' in request.GET:
        end_date = datetime.strptime(request.GET['end_date'], "%Y-%m-%d")
    work_entries_by_employee = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).values('employee').annotate(total_time=Sum('minutes')).order_by('employee')
    context = {
        'work_entries_by_employee': work_entries_by_employee,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    return render(request, 'base/employees.html', context)


@login_required(login_url='login')
def roles(request):
    start_date = date.today().replace(day=1)
    end_date = date.today()
    if 'start_date' in request.GET:
        start_date = datetime.strptime(request.GET['start_date'], "%Y-%m-%d")
    
    if 'end_date' in request.GET:
        end_date = datetime.strptime(request.GET['end_date'], "%Y-%m-%d")
    work_entries_by_role = Work.objects.filter(user=request.user).filter(date__range=[start_date,end_date]).values('role').annotate(total_time=Sum('minutes')).order_by('role')
    context = {
        'work_entries_by_role': work_entries_by_role,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    return render(request, 'base/roles.html', context)

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
        'timesheets': timesheets
    }
    return render(request, 'base/timesheets.html', context)

@login_required(login_url='login')
def my_profile(request):
    return render(request, 'base/my_profile.html')


@login_required(login_url='login')
def help(request):
    return render(request, 'base/help.html')


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
