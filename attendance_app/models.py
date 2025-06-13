from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['code']

class Section(models.Model):
    YEAR_LEVEL_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]
    
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year_level = models.IntegerField(choices=YEAR_LEVEL_CHOICES)
    
    def __str__(self):
        return f"{self.course.code} - {self.name} (Year {self.year_level})"
    
    class Meta:
        unique_together = ('name', 'course', 'year_level')
        ordering = ['course', 'year_level', 'name']

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    YEAR_LEVEL_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]
    
    student_id = models.CharField(max_length=20, unique=True)
    rfid_tag = models.CharField(max_length=50, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    year_level = models.IntegerField(choices=YEAR_LEVEL_CHOICES)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.student_id} - {self.full_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    photo = models.ImageField(upload_to='attendance_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} - {self.date}"
    
    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date', 'student']

class SystemSettings(models.Model):
    system_title = models.CharField(max_length=100, default='Student Monitoring System')
    footer_text = models.CharField(max_length=100, default='CPSC © 2023')
    logo = models.ImageField(upload_to='system_logos/', blank=True, null=True)
    version = models.CharField(max_length=20, default='1.0.0')
    
    def __str__(self):
        return "System Settings"
    
    class Meta:
        verbose_name_plural = "System Settings"

class EmailSettings(models.Model):
    time_in_subject = models.CharField(max_length=100, default='Your child has arrived at school')
    time_in_template = models.TextField(
        default='Dear parent,\n\nYour child {student_name} has arrived at school at {time_in} on {date}.\n\nThank you,\nSchool Administration'
    )
    time_out_subject = models.CharField(max_length=100, default='Your child has left school')
    time_out_template = models.TextField(
        default='Dear parent,\n\nYour child {student_name} has left school at {time_out} on {date}.\n\nThank you,\nSchool Administration'
    )
    smtp_host = models.CharField(max_length=100, default='smtp.gmail.com')
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.CharField(max_length=100)
    smtp_password = models.CharField(max_length=100)
    from_email = models.EmailField(default='noreply@school.edu')
    from_name = models.CharField(max_length=100, default='School Administration')
    
    def __str__(self):
        return "Email Settings"
    
    class Meta:
        verbose_name_plural = "Email Settings"

class SystemLog(models.Model):
    LOG_TYPE_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=10, choices=LOG_TYPE_CHOICES)
    message = models.TextField()
    details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"[{self.log_type.upper()}] {self.timestamp}: {self.message[:50]}"
    
    class Meta:
        ordering = ['-timestamp']

def create_system_settings(sender, **kwargs):
    if not SystemSettings.objects.exists():
        SystemSettings.objects.create()

def create_email_settings(sender, **kwargs):
    if not EmailSettings.objects.exists():
        EmailSettings.objects.create()