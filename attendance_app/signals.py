from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import (
    Student, AttendanceRecord,
    SystemSettings, EmailSettings,
    SystemLog
)
from .utils import log_system_event
import os

@receiver(post_save, sender=Student)
def student_post_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    log_system_event(
        'info',
        f'Student {action}: {instance.full_name}',
        f'Student ID: {instance.student_id}, Section: {instance.section}'
    )

@receiver(post_delete, sender=Student)
def student_post_delete(sender, instance, **kwargs):
    log_system_event(
        'warning',
        f'Student deleted: {instance.full_name}',
        f'Student ID: {instance.student_id}'
    )
    # Delete associated photo file
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)

@receiver(post_save, sender=AttendanceRecord)
def attendance_post_save(sender, instance, created, **kwargs):
    if created:
        log_system_event(
            'info',
            f'Attendance recorded for {instance.student.full_name}',
            f'Date: {instance.date}, Status: {instance.status}'
        )

@receiver(pre_save, sender=SystemSettings)
def delete_old_logo(sender, instance, **kwargs):
    if not instance.pk:
        return False
    
    try:
        old_file = SystemSettings.objects.get(pk=instance.pk).logo
    except SystemSettings.DoesNotExist:
        return False
    
    new_file = instance.logo
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(pre_save, sender=Student)
def delete_old_photo(sender, instance, **kwargs):
    if not instance.pk:
        return False
    
    try:
        old_file = Student.objects.get(pk=instance.pk).photo
    except Student.DoesNotExist:
        return False
    
    new_file = instance.photo
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)