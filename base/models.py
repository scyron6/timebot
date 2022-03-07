from django.db import models

# Create your models here.
class Work(models.Model):
    employee = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    minutes = models.IntegerField()
    date = models.DateField()
    work = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    task = models.CharField(max_length=100)
