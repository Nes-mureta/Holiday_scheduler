# Generated by Django 5.1.2 on 2024-10-30 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_timetable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetable',
            old_name='activity',
            new_name='subject',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='time',
        ),
        migrations.AddField(
            model_name='timetable',
            name='time_slot',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='day',
            field=models.CharField(max_length=20),
        ),
    ]
