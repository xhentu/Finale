from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserCreateForm(UserCreationForm):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'phone_number', 'password1', 'password2']
