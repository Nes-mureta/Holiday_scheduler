from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomLoginForm
from .models import Timetable
import random
from datetime import time, timedelta
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
           # login(request, user)  Automatically logs in the user
            return redirect('login') 
    else:
        form = CustomRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render
from .forms import ProfileForm

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # Redirect or return success response
    else:
        form = ProfileForm(instance=request.user.profile)

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
        '01:00 PM - 02:00 PM',  # Lunch
        '02:00 PM - 03:00 PM', 
        '03:00 PM - 04:00 PM', 
        '04:00 PM - 05:00 PM'
    ]

    if request.method == 'POST':
        subjects = request.POST.getlist('subjects')  # Get subjects from the form
        activity_name = request.POST.get('activity_name')  # Get activity name
        activity_day = request.POST.get('activity_day')  # Get activity day
        activity_time = request.POST.get('activity_time')  # Get activity time slot

        # Clear existing timetables for the user
        Timetable.objects.filter(user=request.user).delete()

        # Create a shuffled list of subjects for each day
        subjects_list = subjects[0].split(',') if subjects else []  # Split the input string by commas
        
        for day in days:
            random.shuffle(subjects_list)  # Shuffle subjects for each day
            subject_index = 0  # Track the current subject index
            
            for time in time_slots:
                if time == '01:00 PM - 02:00 PM':  # Always set as lunch
                    timetable_entry = Timetable(user=request.user, subject='Lunch', day=day, time_slot=time)
                elif time == activity_time and day == activity_day:  # Check for special activity
                    timetable_entry = Timetable(user=request.user, subject=activity_name, day=day, time_slot=time)
                else:
                    # Assign the next subject if available
                    if subject_index < len(subjects_list):
                        subject = subjects_list[subject_index]
                        timetable_entry = Timetable(user=request.user, subject=subject, day=day, time_slot=time)
                        subject_index += 1  # Move to the next subject
                    else:
                        continue  # Skip if no subjects are available

                timetable_entry.save()  # Save each timetable entry
                timetable_entries.append(timetable_entry)

    # Fetch all timetable entries for the current user
    timetable_entries = Timetable.objects.filter(user=request.user)

    # Prepare context for the template
    context = {
        'timetable_entries': timetable_entries,
        'days': days,
        'time_slots': time_slots,
    }
    return render(request, 'generate_timetable.html', context)
def generate_timetable(request):
    timetable_entries = []
    
    # Define days and time slots
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = [
        '08:00 AM - 09:00 AM',
        '09:00 AM - 10:00 AM',
        '10:00 AM - 11:00 AM', 
        '11:00 AM - 12:00 PM', 
        '01:00 PM - 02:00 PM',  # Lunch
        '02:00 PM - 03:00 PM', 
        '03:00 PM - 04:00 PM', 
        '04:00 PM - 05:00 PM'
    ]

    if request.method == 'POST':
        subjects = request.POST.getlist('subjects')  # Get subjects from the form
        activity_names = request.POST.getlist('activity_name')  # Get all activity names
        activity_days = request.POST.getlist('activity_day')  # Get all activity days
        activity_times = request.POST.getlist('activity_time')  # Get all activity time slots

        # Clear existing timetables for the user
        Timetable.objects.filter(user=request.user).delete()

        # Convert the subjects into a list
        subjects_list = subjects[0].split(',') if subjects else []

        # Add special activities to a dictionary for easy access
        special_activities = {
            (day, time): name for name, day, time in zip(activity_names, activity_days, activity_times)
        }

        # Distribute subjects for each day, skipping time slots with special activities
        for day in days:
            random.shuffle(subjects_list)  # Shuffle subjects for each day
            subject_index = 0
            
            for time in time_slots:
                # Set lunch time slot
                if time == '01:00 PM - 02:00 PM':
                    timetable_entry = Timetable(user=request.user, subject='Lunch', day=day, time_slot=time)

                # Check if the slot is a special activity and add it
                elif (day, time) in special_activities:
                    activity_name = special_activities[(day, time)]
                    timetable_entry = Timetable(user=request.user, subject=activity_name, day=day, time_slot=time)
                
                # Add subjects, skipping slots that already contain special activities
                else:
                    if subject_index < len(subjects_list):
                        subject = subjects_list[subject_index]
                        timetable_entry = Timetable(user=request.user, subject=subject, day=day, time_slot=time)
                        subject_index += 1
                    else:
                        continue  # Skip if no more subjects are available

                timetable_entry.save()  # Save each timetable entry
                timetable_entries.append(timetable_entry)

    # Fetch all timetable entries for the current user
    timetable_entries = Timetable.objects.filter(user=request.user)

    # Prepare context for the template
    context = {
        'timetable_entries': timetable_entries,
        'days': days,
        'time_slots': time_slots,
    }
    return render(request, 'generate_timetable.html', context)

def delete_timetable(request):
    # Clear existing timetables for the user
    Timetable.objects.filter(user=request.user).delete()
    return redirect('generate_timetable') 