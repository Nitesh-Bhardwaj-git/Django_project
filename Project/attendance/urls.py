from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('success/', views.attendance_success, name='attendance_success'),
    path('analytics/', views.student_analytics, name='student_analytics'),
    path('qrcodes/', views.student_qrcodes, name='student_qrcodes'),
    path('mark_by_roll/', views.mark_attendance_by_roll, name='mark_attendance_by_roll'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('advanced_analytics/', views.advanced_analytics, name='advanced_analytics'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('history/', views.attendance_history, name='attendance_history'),
    path('export_attendance_history_csv/', views.export_attendance_history_csv, name='export_attendance_history_csv'),
    path('export_student_profile_csv/', views.export_student_profile_csv, name='export_student_profile_csv'),
    path('export_advanced_analytics_csv/', views.export_advanced_analytics_csv, name='export_advanced_analytics_csv'),
    path('bulk_upload/', views.bulk_attendance_upload, name='bulk_attendance_upload'),
] 