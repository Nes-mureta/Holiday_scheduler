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
            return redirect('dashboard') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
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
            return redirect('profile') 
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

@login_required


def generate_timetable(request):
    timetable_entries = []
    
    # Define days and time slots
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
        # Retrieve and parse subjects
        subjects_input = request.POST.get('subjects', '')
        subjects = [subject.strip() for subject in subjects_input.split(',') if subject.strip()]

        # Retrieve special activities (multiple allowed)
        activities = []
        activity_names = request.POST.getlist('activity_name')
        activity_days = request.POST.getlist('activity_day')
        activity_times = request.POST.getlist('activity_time')

        for name, day, time in zip(activity_names, activity_days, activity_times):
            if name and day and time:
                activities.append({'name': name, 'day': day, 'time': time})

        # Clear existing timetables for the user
        Timetable.objects.filter(user=request.user).delete()

        # Loop through each day to populate timetable entries
        for day in days:
            random.shuffle(subjects)  # Shuffle subjects for each day
            subject_index = 0
            free_slots_needed = max(0, len(time_slots) - len(subjects))

            # Fill empty slots with 'Free' if there aren't enough subjects
            subjects_for_day = subjects + ['Free'] * free_slots_needed
            random.shuffle(subjects_for_day)  # Shuffle to randomize 'Free' placements
            
            for time in time_slots:
                # Assign Lunch slot
                if time == '01:00 PM - 02:00 PM':
                    timetable_entry = Timetable(user=request.user, subject='Lunch', day=day, time_slot=time)

                # Assign special activities
                elif any(activity['day'] == day and activity['time'] == time for activity in activities):
                    activity = next(activity for activity in activities if activity['day'] == day and activity['time'] == time)
                    timetable_entry = Timetable(user=request.user, subject=activity['name'], day=day, time_slot=time)

                # Assign subjects or 'Free' to remaining slots
                else:
                    subject = subjects_for_day[subject_index]
                    timetable_entry = Timetable(user=request.user, subject=subject, day=day, time_slot=time)
                    subject_index = (subject_index + 1) % len(subjects_for_day)

                # Save and add entry to the list
                timetable_entry.save()
                timetable_entries.append(timetable_entry)

    # Retrieve timetable entries for the user to display in template
    timetable_entries = Timetable.objects.filter(user=request.user)
    
  
    # Prepare events for calendar display
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

    # Pass context to the template
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


from django.http import JsonResponse

def update_timetable(request):
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        completed = request.POST.get('completed') == 'true'
        try:
            entry = Timetable.objects.get(id=entry_id)
            entry.completed = completed
            entry.save()
            return JsonResponse({'status': 'success'})
        except Timetable.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Entry not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def dashboard(request):
    profile,created = Profile.objects.get_or_create(user=request.user)
    
    if not profile.full_name:
        profile.full_name = request.user.username()
        profile.save()
    
    
    context = {
        'profile': profile,
        'timetable_entries': timetable_entries,
        'profile_complete': profile_complete,
    }
    return render(request, 'dashboard.html', context)


import calendar
from django.utils import timezone

@login_required
def dashboard(request):
    current_date = timezone.now().date() 
    current_day = datetime.now().strftime('%A')  # Get the current day name
    todays_subjects = Timetable.objects.filter(user=request.user, day__iexact=current_day)  # Use __iexact for case-insensitive match
     
   # Debugging statement
    print(f"Current day: {current_day}")
    print(f"Today's subjects: {todays_subjects}")
    
    # Create a calendar for the current month
    month_calendar = calendar.monthcalendar(current_date.year, current_date.month)
    
    # Generate the grid layout for the calendar
    days_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    calendar_html = '<div class="grid grid-cols-7 gap-1">'
    
    # Add the days of the week header
    for day_name in days_names:
        calendar_html += f'<div class="font-normal font-xs gap-1 text-center">{day_name}</div>'

    # Highlight the current day
    for week in month_calendar:
        for day in week:
            if day == 0: 
                calendar_html += '<div class="text-center text-gray-400"></div>'
            else:
                if day == current_date.day and current_date.month == current_date.month:
                    calendar_html += f'<div class="bg-red-500 text-center font-normal">{day}</div>'
                else:
                    calendar_html += f'<div class="text-center">{day}</div>'
    
    calendar_html += '</div>'  # Close the grid container

    context = {
        'todays_subjects': todays_subjects,
        'profile': request.user.profile,
        'current_date': current_date,
        'month_calendar': calendar_html,  # Pass the custom calendar HTML to the template
    }
    return render(request, 'dashboard.html', context)