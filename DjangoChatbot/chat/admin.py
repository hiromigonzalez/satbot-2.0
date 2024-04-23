# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Document, Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'semester']
    search_fields = ['name', 'year', 'semester']
    list_filter = ['year', 'semester']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_at', 'course_name', 'document_link']
    list_filter = ['course__name']  # Allow filtering by course name in the admin
    readonly_fields = ['uploaded_at', 'document_link']

    def document_link(self, obj):
        if obj.docfile:
            return format_html("<a href='{}'>Download</a>", obj.docfile.url)
        return "No file"

    def course_name(self, obj):
        return obj.course.name if obj.course else "General"
    document_link.short_description = "Document"
    course_name.short_description = "Course"
    fieldsets = (
        (None, {
            'fields': ('name', 'docfile', 'course')
        }),
        ('Timestamp', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
