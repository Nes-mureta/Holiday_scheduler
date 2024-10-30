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

    if request.method == 'POST':
        subjects = request.POST.getlist('subjects')  # Get subjects from the form
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        time_slots = [
            '08:00 AM - 09:00 AM',
            '09:00 AM - 10:00 AM',
            '10:00 AM - 11:00 AM', 
            '11:00 AM - 12:00 PM', 
            '01:00 PM - 02:00 PM',  # Lunch slot
            '02:00 PM - 03:00 PM', 
            '03:00 PM - 04:00 PM', 
            '04:00 PM - 05:00 PM'
        ]

        # Clear existing timetables for the user
        Timetable.objects.filter(user=request.user).delete()

        # Create a shuffled list of subjects for each day
        subjects_list = subjects[0].split(',')  # Split the input string by commas

        for day in days:
            random.shuffle(subjects_list)  # Shuffle subjects for each day
            
            for i, time in enumerate(time_slots):
                # Assign "Lunch" for the 1 PM - 2 PM time slot
                if time == '01:00 PM - 02:00 PM':
                    subject = "Lunch"
                else:
                    subject = subjects_list[i % len(subjects_list)]  # Rotate through the subjects

                # Create and save the timetable entry
                timetable_entry = Timetable(user=request.user, subject=subject, day=day, time_slot=time)
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