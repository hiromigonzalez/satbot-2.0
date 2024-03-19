from django.contrib import admin
from .models import Course, User

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'semester']
    search_fields = ['name', 'year', 'semester']  # Optional: Add search capability
    list_filter = ['year', 'semester']  # Optional: Add filters on the side

"""
@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'course']
"""
