from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Course, User

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    course_name = forms.CharField(required=False)
    year = forms.IntegerField(required=False)
    semester = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'role')

    def clean(self):
        cleaned_data = super().clean()
        course_name = cleaned_data.get('course_name')
        year = cleaned_data.get('year')
        semester = cleaned_data.get('semester')

        if course_name and year and semester:
            try:
                course = Course.objects.get(name=course_name, year=year, semester=semester)
                cleaned_data['course'] = course
            except Course.DoesNotExist:
                self.add_error(None, _('The specified course does not exist.'))
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _("USD Username")
        self.fields['email'].label = _("USD Email")
        self.fields['username'].help_text = ""
        self.fields['password2'].help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        # Assuming 'course' is correctly related to the User model
        course = self.cleaned_data.get('course', None)
        if course:
            user.course = course
        if commit:
            user.save()
            self.save_m2m()
