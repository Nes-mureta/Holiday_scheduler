from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('generate-timetable/', views.generate_timetable, name='generate_timetable'),
    path('delete-timetable/', views.delete_timetable, name='delete_timetable'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
