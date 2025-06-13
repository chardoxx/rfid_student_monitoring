from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, date, timedelta
import json
import os
from .models import (
    Course, Section, Student,
    AttendanceRecord, SystemSettings,
    EmailSettings, SystemLog
)
from .forms import (
    CourseForm, SectionForm, StudentForm,
    StudentImportForm, SystemSettingsForm,
    EmailSettingsForm, TestEmailForm,
    UserRegistrationForm, ProfileUpdateForm,
    CustomPasswordChangeForm
)
from .utils import (
    send_attendance_email, log_system_event,
    process_student_import, get_dashboard_stats
)
import tempfile

# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if 'remember' not in request.POST:
                request.session.set_expiry(0)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'attendance_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'attendance_app/register.html', {'form': form})

# Admin Views
@login_required
def admin_dashboard(request):
    stats = get_dashboard_stats()
    return render(request, 'attendance_app/admin/dashboard.html', stats)

@login_required
def course_list(request):
    courses = Course.objects.all().order_by('code')
    return render(request, 'attendance_app/admin/courses.html', {'courses': courses})

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully')
            return redirect('courses')
    else:
        form = CourseForm()
    
    return render(request, 'attendance_app/admin/courses.html', {'form': form})

@login_required
def edit_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully')
            return redirect('courses')
    return redirect('courses')

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully')
    return redirect('courses')

@login_required
def section_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    sections = Section.objects.filter(course=course).order_by('year_level', 'name')
    return render(request, 'attendance_app/admin/sections.html', {
        'course': course,
        'sections': sections
    })

@login_required
def add_section(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            section.save()
            messages.success(request, 'Section added successfully')
            return redirect('view_sections', course_id=course.id)
    else:
        form = SectionForm()
    
    return render(request, 'attendance_app/admin/sections.html', {
        'course': course,
        'form': form
    })

@login_required
def edit_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section updated successfully')
            return redirect('view_sections', course_id=section.course.id)
    else:
        form = SectionForm(instance=section)
    
    return render(request, 'attendance_app/admin/sections.html', {
        'course': section.course,
        'form': form,
        'editing': True
    })

@login_required
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    course_id = section.course.id
    if request.method == 'POST':
        section.delete()
        messages.success(request, 'Section deleted successfully')
    return redirect('view_sections', course_id=course_id)

@login_required
def student_list(request):
    students = Student.objects.select_related('section').order_by('last_name', 'first_name')
    
    # Filtering
    search_query = request.GET.get('search', '')
    year_level = request.GET.get('year_level', '')
    section_id = request.GET.get('section', '')
    
    if search_query:
        students = students.filter(
            Q(student_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if year_level:
        students = students.filter(year_level=year_level)
    
    if section_id:
        students = students.filter(section_id=section_id)
    
    # Pagination
    paginator = Paginator(students, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    all_sections = Section.objects.all().order_by('name')
    
    return render(request, 'attendance_app/admin/students.html', {
        'students': page_obj,
        'all_sections': all_sections,
        'search_query': search_query,
        'selected_year': year_level,
        'selected_section': section_id
    })

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} added successfully')
            return redirect('students')
    else:
        form = StudentForm()
    
    all_sections = Section.objects.all().order_by('name')
    return render(request, 'attendance_app/admin/students.html', {
        'form': form,
        'all_sections': all_sections
    })

@login_required
def edit_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student {student.full_name} updated successfully')
            return redirect('students')
    return redirect('students')

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully')
    return redirect('students')

@login_required
def import_students(request):
    if request.method == 'POST':
        form = StudentImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file temporarily
            excel_file = request.FILES['excel_file']
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in excel_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name
            
            # Process the file
            result = process_student_import(
                tmp_file_path,
                form.cleaned_data['update_existing']
            )
            
            if result['success']:
                msg = (
                    f"Import successful: {result['imported']} imported, "
                    f"{result['updated']} updated, {result['skipped']} skipped"
                )
                messages.success(request, msg)
            else:
                messages.error(request, f"Import failed: {result['error']}")
            
            return redirect('students')
    else:
        form = StudentImportForm()
    
    return render(request, 'attendance_app/admin/students.html', {'import_form': form})

@login_required
def attendance_reports(request):
    # Default to last 7 days
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    section_id = request.GET.get('section')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = date.today() - timedelta(days=7)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = date.today()
    
    records = AttendanceRecord.objects.select_related('student', 'student__section').filter(
        date__range=[start_date, end_date]
    ).order_by('-date', 'student__last_name')
    
    if section_id:
        records = records.filter(student__section_id=section_id)
    
    # Get unique sections for filter dropdown
    all_sections = Section.objects.all().order_by('name')
    
    # Pagination
    paginator = Paginator(records, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'attendance_app/admin/reports.html', {
        'attendance_records': page_obj,
        'all_sections': all_sections,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'selected_section': section_id
    })

# Settings Views
@login_required
def settings_view(request):
    return redirect('profile_settings')

@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_settings')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'attendance_app/admin/settings/profile.html', {'form': form})

@login_required
def email_settings(request):
    email_settings, created = EmailSettings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        form = EmailSettingsForm(request.POST, instance=email_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email settings updated successfully')
            return redirect('email_settings')
    else:
        form = EmailSettingsForm(instance=email_settings)
    
    return render(request, 'attendance_app/admin/settings/email_setup.html', {
        'form': form,
        'test_form': TestEmailForm()
    })

@login_required
def system_settings(request):
    system_settings, created = SystemSettings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        form = SystemSettingsForm(request.POST, request.FILES, instance=system_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'System settings updated successfully')
            return redirect('system_settings')
    else:
        form = SystemSettingsForm(instance=system_settings)
    
    return render(request, 'attendance_app/admin/settings/system_info.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully')
            return redirect('profile_settings')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'attendance_app/admin/settings/profile.html', {'password_form': form})

@login_required
def send_test_email(request):
    if request.method == 'POST':
        form = TestEmailForm(request.POST)
        if form.is_valid():
            # Create a test attendance record
            student = Student(
                first_name="Test",
                last_name="Student",
                section=Section.objects.first(),
                year_level=1,
                student_id="TEST001",
                guardian_email=form.cleaned_data['test_email']
            )
            
            record = AttendanceRecord(
                student=student,
                date=date.today(),
                time_in=datetime.now().time(),
                status='present'
            )
            
            # Send test email
            success = send_attendance_email(
                student, 
                record, 
                form.cleaned_data['test_type']
            )
            
            if success:
                messages.success(request, 'Test email sent successfully')
            else:
                messages.error(request, 'Failed to send test email')
    
    return redirect('email_settings')

# Kiosk Views
def attendance_kiosk(request):
    return render(request, 'attendance_app/kiosk.html')

@csrf_exempt
def log_attendance(request, rfid_tag):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    try:
        student = Student.objects.get(rfid_tag=rfid_tag)
        today = date.today()
        
        # Check if there's an existing record for today
        record, created = AttendanceRecord.objects.get_or_create(
            student=student,
            date=today,
            defaults={'status': 'present'}
        )
        
        # Update time in/out
        now = datetime.now().time()
        if not record.time_in:
            record.time_in = now
            record.status = 'present'
            email_type = 'time_in'
        elif not record.time_out:
            record.time_out = now
            email_type = 'time_out'
        else:
            # Already logged in and out today
            return JsonResponse({
                'success': True,
                'student_name': student.full_name,
                'student_id': student.student_id,
                'photo_url': student.photo.url if student.photo else '',
                'time_in': record.time_in.strftime('%I:%M %p'),
                'time_out': record.time_out.strftime('%I:%M %p'),
                'message': 'Attendance already recorded for today'
            })
        
        record.save()
        
        # Send email notification
        send_attendance_email(student, record, email_type)
        
        return JsonResponse({
            'success': True,
            'student_name': student.full_name,
            'student_id': student.student_id,
            'photo_url': student.photo.url if student.photo else '',
            'time_in': record.time_in.strftime('%I:%M %p') if record.time_in else '--:--',
            'time_out': record.time_out.strftime('%I:%M %p') if record.time_out else '--:--',
            'message': 'Attendance recorded successfully'
        })
        
    except Student.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Student not found with this RFID tag'
        })
    except Exception as e:
        log_system_event('error', 'Failed to log attendance', str(e))
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# API Views
def get_sections_by_year(request, year_level):
    sections = Section.objects.filter(year_level=year_level).values('id', 'name')
    return JsonResponse(list(sections), safe=False)