from django.contrib.auth.models import AbstractUser
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    semester = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - Year {self.year} - {self.semester}"

class User(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='student')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    def __str__(self):
        return self.username
"""
class Intent(models.Model):
    question = models.TextField()
    answer = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.question
"""