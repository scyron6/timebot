from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Work(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.CharField(max_length=100, blank=True)
    client = models.CharField(max_length=100, blank=True)
    minutes = models.IntegerField(blank=True)
    date = models.DateField(blank=True)
    work = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    task = models.CharField(max_length=100, blank=True)
