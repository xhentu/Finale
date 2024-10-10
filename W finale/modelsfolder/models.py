# Base CustomUser model to extend from AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models

# Base CustomUser model to extend from AbstractUser
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)

    # Override related_name for groups and user_permissions to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Add custom related_name here
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Add custom related_name here
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# 1. Admin Profile (Optional fields)
class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="admin_profile")
    # Add more fields if needed, such as permissions or settings

# 2. Teacher Profile and Related Models
class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_profile")
    subject = models.CharField(max_length=100)
    hire_date = models.DateField()

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="courses")
    schedule = models.DateTimeField()

class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="classes")
    students = models.ManyToManyField('StudentProfile', related_name="classes")
    room_number = models.CharField(max_length=10)

# 3. Staff Profile and Fee Management
class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="staff_profile")
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

class Fee(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name="fees")
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)

# 4. Parent Profile and Parent-Teacher Meeting
class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="parent_profile")
    children = models.ManyToManyField('StudentProfile', related_name="parents")

class ParentTeacherMeeting(models.Model):
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name="meetings")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="meetings")
    scheduled_date = models.DateTimeField()
    topic = models.CharField(max_length=255)

# 5. Student Profile and Related Models
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    parent = models.ForeignKey(ParentProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="children_students")
    enrollment_date = models.DateField()
    grade_level = models.CharField(max_length=20)

class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendances")
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))

class Grade(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades")
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)
