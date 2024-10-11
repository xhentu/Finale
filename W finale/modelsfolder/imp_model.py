from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. CustomUser Model (with indexed role and unique phone number)
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, db_index=True)
    phone_number = models.CharField(max_length=15, blank=True, unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_permissions",
        blank=True,
    )

# 2. Base Profile for common fields
class BaseProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="%(class)s_profile")
    hire_date = models.DateField()

    class Meta:
        abstract = True

# 3. Admin Profile
class AdminProfile(BaseProfile):
    class Meta:
        permissions = [
            ("manage_staff", "Can manage staff members"),
            ("manage_teachers", "Can manage teachers and their settings"),
        ]

# 4. Staff Profile
class StaffProfile(BaseProfile):
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("manage_students", "Can manage student profiles and data"),
            ("manage_classes", "Can manage classes and class-related settings"),
            ("manage_fees", "Can manage fee payments and related information"),
        ]

# 5. Teacher Profile
class TeacherProfile(BaseProfile):
    main_subject = models.CharField(max_length=100)
    additional_subjects = models.ManyToManyField('Subject', blank=True, related_name='additional_teachers')

    class Meta:
        permissions = [
            ("manage_attendance", "Can manage attendance records"),
            ("manage_grades", "Can manage grades and exams"),
            ("manage_class_schedule", "Can manage class schedule and timetable"),
        ]

# 6. Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

# 7. Class Model
class Class(models.Model):
    title = models.CharField(max_length=100)
    assigned_teacher = models.ForeignKey('TeacherProfile', on_delete=models.SET_NULL, null=True, related_name="assigned_classes")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name="classes")
    students = models.ManyToManyField('StudentProfile', related_name="classes")  # Use string reference for StudentProfile
    room_number = models.CharField(max_length=10)
    schedule = models.ForeignKey('Schedule', on_delete=models.SET_NULL, null=True, related_name="classes")

# 8. Schedule Model
class Schedule(models.Model):
    SECTION_CHOICES = [
        ('1st Section', '9:00 am - 10:30 am'),
        ('2nd Section', '10:45 am - 12:15 pm'),
        ('3rd Section', '12:45 pm - 1:15 pm'),
        ('4th Section', '2:00 pm - 3:30 pm'),
    ]
    class_instance = models.ForeignKey('Class', on_delete=models.CASCADE, related_name="timetable")
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True, related_name="scheduled_sections")
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ])

    class Meta:
        unique_together = ('class_instance', 'day_of_week', 'section')

# 9. Student Profile
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    class_instance = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, related_name="enrolled_students")  # Unique related name
    parent = models.ForeignKey('ParentProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name="children_students")
    enrollment_date = models.DateField()
    grade_level = models.CharField(max_length=20)

    class Meta:
        permissions = [
            ("view_class_schedule", "Can view class schedule"),
            ("view_grades", "Can view grades"),
        ]

# 10. Parent Profile
class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="parent_profile")
    children = models.ManyToManyField('StudentProfile', related_name="parents")

    class Meta:
        permissions = [
            ("view_child_progress", "Can view their child's progress and related data"),
        ]

# 11. Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name="attendances")
    class_instance = models.ForeignKey('Class', on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))

# 12. Exam Model
class Exam(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name="exams")
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name="exams")
    date = models.DateField()
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('subject', 'student', 'date')

# 13. Grade Model
class Grade(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name="grades")
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, related_name="grades")
    grade_value = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)

# 14. Fee Model
class Fee(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name="fees")
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(db_index=True)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
