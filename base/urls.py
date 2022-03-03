from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginPage, name='login'),

    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/clients/', views.clients, name='clients'),
    path('dashboard/employees/', views.employees, name='employees'),
    path('dashboard/roles/', views.roles, name='roles'),
    path('dashboard/my_profile/', views.my_profile, name='my_profile'),
]