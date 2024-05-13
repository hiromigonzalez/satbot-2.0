#models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import os

from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    semester = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - Year {self.year} - {self.semester}"
    
def document_directory_path(instance, filename):
    # Determine the subdirectory based on course selection
    if instance.is_general():
        subdirectory = 'general'
    else:
        subdirectory = str(instance.course.id)

    # Join the subdirectory and filename to get the full path
    return os.path.join('documents', subdirectory, filename)
    
class Document(models.Model):
    name = models.CharField(max_length=255, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    docfile = models.FileField(upload_to=document_directory_path)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')

    def __str__(self):
        return self.name

    def is_general(self):
        return self.course is None

class User(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='student')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    def __str__(self):
        return self.username
    