from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Admin Views
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('courses/', views.course_list, name='courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('sections/<int:course_id>/', views.section_list, name='view_sections'),
    path('sections/add/<int:course_id>/', views.add_section, name='add_section'),
    path('sections/edit/<int:section_id>/', views.edit_section, name='edit_section'),
    path('sections/delete/<int:section_id>/', views.delete_section, name='delete_section'),
    
    # Student Management
    path('students/', views.student_list, name='students'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('students/import/', views.import_students, name='import_students'),
    
    # Reports
    path('reports/', views.attendance_reports, name='reports'),
    
    # Settings
    path('settings/', views.settings_view, name='settings'),
    path('settings/profile/', views.profile_settings, name='profile_settings'),
    path('settings/email/', views.email_settings, name='email_settings'),
    path('settings/system/', views.system_settings, name='system_settings'),
    path('settings/change-password/', views.change_password, name='change_password'),
    path('settings/send-test-email/', views.send_test_email, name='send_test_email'),
    
    # Kiosk
    path('kiosk/', views.attendance_kiosk, name='kiosk'),
    path('api/attendance/log/<str:rfid_tag>/', views.log_attendance, name='log_attendance'),
    
    # API Endpoints
    path('api/sections/<int:year_level>/', views.get_sections_by_year, name='get_sections_by_year'),
]