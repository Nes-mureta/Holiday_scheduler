from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.custom_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('generate-timetable/', views.generate_timetable, name='generate_timetable'),
    path('delete-timetable/', views.delete_timetable, name='delete_timetable'),
    path('dashboard/', views.dashboard, name='dashboard'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)