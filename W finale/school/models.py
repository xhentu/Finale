from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save  # Import post_save
from django.dispatch import receiver  # Import receiver

# CustomUser model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# Profile model for Admin
class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add any specific fields for Admins
    def __str__(self):
        return f'{self.user.username} (Admin)'

# Profile model for Staff
class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add any specific fields for Staff
    def __str__(self):
        return f'{self.user.username} (Staff)'

# Profile model for Teachers
class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add any specific fields for Teachers
    def __str__(self):
        return f'{self.user.username} (Teacher)'

# Profile model for Students
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add any specific fields for Students
    def __str__(self):
        return f'{self.user.username} (Student)'

# Profile model for Parents
class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add any specific fields for Parents
    def __str__(self):
        return f'{self.user.username} (Parent)'
