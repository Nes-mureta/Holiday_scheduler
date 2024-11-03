from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm,ProfileForm
from .models import Timetable,Profile
import random
from datetime import time, timedelta,datetime
from django.contrib.auth.decorators import login_required

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile 
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

@login_required

def generate_timetable(request):
    timetable_entries = []
    
    # Define days and time slots at the beginning
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = [
        '08:00 AM - 09:00 AM',
        '09:00 AM - 10:00 AM',
        '10:00 AM - 11:00 AM', 
        '11:00 AM - 12:00 PM', 
        '01:00 PM - 02:00 PM',  
        '02:00 PM - 03:00 PM', 
        '03:00 PM - 04:00 PM', 
        '04:00 PM - 05:00 PM'
    ]

    if request.method == 'POST':
        subjects = request.POST.getlist('subjects')  
        activity_name = request.POST.get('activity_name')  
        activity_day = request.POST.get('activity_day') 
        activity_time = request.POST.get('activity_time') 

        # Clear existing timetables for the user
        Timetable.objects.filter(user=request.user).delete()

        # Create a shuffled list of subjects for each day
        subjects_list = subjects[0].split(',') if subjects else []  # Split the input string by commas
        
        for day in days:
            random.shuffle(subjects_list) 
            subject_index = 0 
            
            for time in time_slots:
                if time == '01:00 PM - 02:00 PM': 
                    timetable_entry = Timetable(user=request.user, subject='Lunch', day=day, time_slot=time)
                elif time == activity_time and day == activity_day: 
                    timetable_entry = Timetable(user=request.user, subject=activity_name, day=day, time_slot=time)
                else:
                    if subject_index < len(subjects_list):
                        subject = subjects_list[subject_index]
                        timetable_entry = Timetable(user=request.user, subject=subject, day=day, time_slot=time)
                        subject_index += 1  
                    else:
                        continue 

                timetable_entry.save()  
                timetable_entries.append(timetable_entry)

    # Process each entry's time slot for calendar events
    events = []
    for entry in timetable_entries:
        start_time, end_time = entry.time_slot.split(" - ")
        start_datetime = datetime.strptime(f"{entry.day} {start_time}", "%A %I:%M %p")
        end_datetime = datetime.strptime(f"{entry.day} {end_time}", "%A %I:%M %p")
        
        events.append({
            'title': entry.subject,
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
        })

    # Fetch all timetable entries for the current user
    timetable_entries = Timetable.objects.filter(user=request.user)

    context = {
        'timetable_entries': timetable_entries,
        'days': days,
        'time_slots': time_slots,
        'events': events,
    }
    return render(request, 'generate_timetable.html', context)

def delete_timetable(request):
    Timetable.objects.filter(user=request.user).delete()
    return redirect('generate_timetable') 


def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    timetable_entries = Timetable.objects.filter(user=request.user)
    
    context = {
        'profile': profile,
        'timetable_entries': timetable_entries,
    }
    return render(request, 'dashboard.html', context)


import calendar
from django.utils import timezone

def dashboard(request):
    current_date = timezone.now().date()  

    # Create a calendar for the current month
    month_calendar = calendar.monthcalendar(current_date.year, current_date.month)
    
    # Generate the grid layout for the calendar
    days_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    calendar_html = '<div class="grid grid-cols-7 gap-2">'
    
    # Add the days of the week header
    for day_name in days_names:
        calendar_html += f'<div class="font-bold text-center">{day_name}</div>'

    # Highlight the current day
    for week in month_calendar:
        for day in week:
            if day == 0: 
                calendar_html += '<div class="text-center text-gray-400"></div>'
            else:
                if day == current_date.day and current_date.month == current_date.month:
                    calendar_html += f'<div class="bg-yellow-300 text-center font-bold">{day}</div>'
                else:
                    calendar_html += f'<div class="text-center">{day}</div>'
    
    calendar_html += '</div>'  # Close the grid container

    context = {
        'profile': request.user.profile,
        'current_date': current_date,
        'month_calendar': calendar_html,  # Pass the custom calendar HTML to the template
    }
    return render(request, 'dashboard.html', context)