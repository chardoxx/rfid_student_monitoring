from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from .models import SystemLog, EmailSettings
import logging
import xlrd
from datetime import datetime
import os
from attendance_app.models import Student
from attendance_app.models import AttendanceRecord  # Add this line

logger = logging.getLogger(__name__)

def send_attendance_email(student, record, email_type):
    """Send attendance notification email to parent/guardian"""
    try:
        email_settings = EmailSettings.objects.first()
        if not email_settings:
            logger.error("Email settings not configured")
            return False
        
        if email_type == 'time_in':
            subject = email_settings.time_in_subject
            template = email_settings.time_in_template
            time_field = record.time_in.strftime('%I:%M %p') if record.time_in else '--:--'
        else:
            subject = email_settings.time_out_subject
            template = email_settings.time_out_template
            time_field = record.time_out.strftime('%I:%M %p') if record.time_out else '--:--'
        
        # Format the email template with student data
        email_body = template.format(
            student_name=student.full_name,
            time_in=record.time_in.strftime('%I:%M %p') if record.time_in else '--:--',
            time_out=record.time_out.strftime('%I:%M %p') if record.time_out else '--:--',
            time=time_field,
            date=record.date.strftime('%B %d, %Y'),
            section=student.section.name
        )
        
        recipient_email = student.guardian_email or student.email
        if not recipient_email:
            logger.warning(f"No email address for {student.full_name}")
            return False
        
        send_mail(
            subject=subject,
            message=email_body,
            from_email=f"{email_settings.from_name} <{email_settings.from_email}>",
            recipient_list=[recipient_email],
            fail_silently=False,
            auth_user=email_settings.smtp_username,
            auth_password=email_settings.smtp_password,
            connection=None
        )
        
        return True
    except Exception as e:
        logger.error(f"Error sending attendance email: {e}")
        SystemLog.objects.create(
            log_type='error',
            message='Failed to send attendance email',
            details=str(e)
        )
        return False

def log_system_event(log_type, message, details=None):
    """Log system events to database"""
    SystemLog.objects.create(
        log_type=log_type,
        message=message,
        details=details
    )

def process_student_import(file_path, update_existing=False):
    """Process imported student data from Excel file"""
    try:
        workbook = xlrd.open_workbook(file_path)
        sheet = workbook.sheet_by_index(0)
        
        # Get headers
        headers = [sheet.cell_value(0, col) for col in range(sheet.ncols)]
        
        required_columns = ['student_id', 'first_name', 'last_name', 'year_level', 'section']
        for col in required_columns:
            if col not in headers:
                raise ValueError(f"Missing required column: {col}")
        
        # Process rows
        imported = 0
        updated = 0
        skipped = 0
        
        for row in range(1, sheet.nrows):
            try:
                row_data = dict(zip(headers, [sheet.cell_value(row, col) for col in range(sheet.ncols)]))
                
                # Get or create student
                student_id = str(row_data['student_id']).strip()
                if not student_id:
                    skipped += 1
                    continue
                
                # Get section
                section_name = str(row_data['section']).strip()
                year_level = int(row_data['year_level'])
                
                section = Section.objects.filter(
                    name__iexact=section_name,
                    year_level=year_level
                ).first()
                
                if not section:
                    skipped += 1
                    continue
                
                # Prepare student data
                student_data = {
                    'student_id': student_id,
                    'first_name': str(row_data['first_name']).strip(),
                    'last_name': str(row_data['last_name']).strip(),
                    'year_level': year_level,
                    'section': section,
                }
                
                # Optional fields
                if 'rfid_tag' in row_data:
                    student_data['rfid_tag'] = str(row_data['rfid_tag']).strip() or None
                if 'email' in row_data:
                    student_data['email'] = str(row_data['email']).strip() or None
                if 'guardian_email' in row_data:
                    student_data['guardian_email'] = str(row_data['guardian_email']).strip() or None
                if 'birthday' in row_data:
                    try:
                        if isinstance(row_data['birthday'], float):
                            # Convert Excel date number to Python date
                            birthday = xlrd.xldate.xldate_as_datetime(row_data['birthday'], workbook.datemode)
                            student_data['birthday'] = birthday.date()
                        else:
                            student_data['birthday'] = datetime.strptime(row_data['birthday'], '%Y-%m-%d').date()
                    except (ValueError, TypeError):
                        student_data['birthday'] = None
                
                # Create or update student
                if update_existing:
                    student, created = Student.objects.update_or_create(
                        student_id=student_id,
                        defaults=student_data
                    )
                    if created:
                        imported += 1
                    else:
                        updated += 1
                else:
                    if not Student.objects.filter(student_id=student_id).exists():
                        Student.objects.create(**student_data)
                        imported += 1
                    else:
                        skipped += 1
                        
            except Exception as e:
                logger.error(f"Error processing row {row}: {e}")
                skipped += 1
                continue
        
        # Clean up
        os.remove(file_path)
        
        return {
            'success': True,
            'imported': imported,
            'updated': updated,
            'skipped': skipped
        }
        
    except Exception as e:
        logger.error(f"Error processing import file: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return {
            'success': False,
            'error': str(e)
        }

def get_dashboard_stats():
    """Get statistics for the admin dashboard"""
    from django.db.models import Count, Q
    from datetime import date
    
    today = date.today()
    
    stats = {
        'total_students': Student.objects.count(),
        'today_logs_count': AttendanceRecord.objects.filter(date=today).count(),
        'present_today': AttendanceRecord.objects.filter(
            date=today, 
            status='present'
        ).count(),
        'absent_today': Student.objects.count() - AttendanceRecord.objects.filter(
            date=today
        ).values('student').distinct().count(),
        'recent_logins': AttendanceRecord.objects.select_related('student')
            .filter(date=today)
            .order_by('-time_in')[:8]
    }
    
    return stats