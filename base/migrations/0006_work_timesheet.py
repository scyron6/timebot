# Generated by Django 4.0.3 on 2022-03-08 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_work_timesheet'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='timesheet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.timesheet'),
            preserve_default=False,
        ),
    ]