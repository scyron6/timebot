from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.db.models import Sum

from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from .bot import bot
from .models import Work


def index(request):
    return render(request, 'base/index.html')


@login_required(login_url='login')
def dashboard(request):
    if request.method == 'POST':
        files = request.FILES.getlist('excel_timesheets')
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        wb = bot.run(files, start_date, end_date)
        filename = 'attachment; filename="Timesheet Summary ' + \
            start_date + ' - ' + end_date + '.xls"'
        response = HttpResponse(save_virtual_workbook(
            wb), headers={
                'Content_Type': 'application/vnd.ms-excel',
                'Content-Disposition': filename,
        })

        return response
    
    total_clients = Work.objects.filter(user=request.user).values('client').distinct().count()
    total_minutes = Work.objects.filter(user=request.user).aggregate(Sum('minutes'))
    total_employees = Work.objects.filter(user=request.user).values('employee').distinct().count()
    total_roles = Work.objects.filter(user=request.user).values('role').distinct().count()
    work_entries_by_client = Work.objects.filter(user=request.user).values('client').annotate(total_time=Sum('minutes')).order_by('-total_time')[:5]
    work_entries_by_employee = Work.objects.filter(user=request.user).values('employee').order_by('employee').annotate(total_time=Sum('minutes'))
    work_entries_by_role = Work.objects.filter(user=request.user).values('role').annotate(total_time=Sum('minutes')).order_by('-total_time')[:5]
    context = {
        'total_clients': total_clients,
        'total_minutes': total_minutes,
        'total_employees': total_employees,
        'total_roles': total_roles,
        'work_entries_by_client': work_entries_by_client,
        'work_entries_by_employee': work_entries_by_employee,
        'work_entries_by_role': work_entries_by_role
    }
    return render(request, 'base/dashboard2.html', context)


@login_required(login_url='login')
def clients(request):
    return render(request, 'base/clients.html')


@login_required(login_url='login')
def employees(request):
    return render(request, 'base/employees.html')


@login_required(login_url='login')
def roles(request):
    return render(request, 'base/roles.html')


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
