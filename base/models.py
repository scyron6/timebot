from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    submission_date = models.DateField(blank=True)

class Work(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE)
    employee = models.CharField(max_length=100, blank=True)
    client = models.CharField(max_length=100, blank=True)
    minutes = models.IntegerField(blank=True)
    date = models.DateField(blank=True)
    work = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    task = models.CharField(max_length=100, blank=True)
