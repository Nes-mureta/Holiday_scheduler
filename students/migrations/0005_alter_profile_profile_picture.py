# Generated by Django 5.1.2 on 2024-10-30 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_timetable_special_time_timetable_time_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='https://www.shutterstock.com/shutterstock/photos/738763984/display_1500/stock-vector-default-unisex-profile-icon-framed-flat-vector-graphic-on-isolated-background-738763984.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
