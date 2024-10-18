from django.contrib.auth.models import AbstractUser
from django.db import models

# Base CustomUser model with role field
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)

    class Meta:
        permissions = [
            ("can_create_staff", "Can create staff members"),
            ("can_manage_teachers", "Can manage teachers"),
            ("can_view_all_data", "Can view all data"),
        ]

# Staff Profile model
class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="staff_profile")
    hire_date = models.DateField()
    department = models.CharField(max_length=100)
    
    class Meta:
        permissions = [
            ("can_manage_students", "Can manage students"),
            ("can_manage_parents", "Can manage parents"),
            ("can_manage_fees", "Can manage fees"),
            ("can_manage_classes", "Can manage classes"),
        ]

# Teacher Profile model
class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_profile")
    hire_date = models.DateField()
    main_subject = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("can_manage_attendance", "Can manage attendance"),
            ("can_manage_exam", "Can manage exam"),
            ("can_manage_grades", "Can manage grades"),
            ("can_manage_schedule", "Can manage class schedule"),
        ]

# Class model to represent a class, with teacher and student relationships
class Class(models.Model):
    title = models.CharField(max_length=100)
    assigned_teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="assigned_classes")
    students = models.ManyToManyField('StudentProfile', related_name="enrolled_classes")
    room_number = models.CharField(max_length=10)

# Student Profile model
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    enrollment_date = models.DateField()
    grade_level = models.CharField(max_length=20)
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name="students_in_class")

# Parent Profile model
class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="parent_profile")
    children = models.ManyToManyField(StudentProfile, related_name="parents")

# Attendance model
class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendances")
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="class_attendances")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))

# Exam model
class Exam(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="class_exams")
    subject = models.CharField(max_length=100)
    date = models.DateField()
    max_marks = models.IntegerField()

# Grade model
class Grade(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="grades")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="exam_grades")
    obtained_marks = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)
