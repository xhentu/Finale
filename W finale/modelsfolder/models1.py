from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. Custom User Model for All User Types
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

    class Meta:
        permissions = [
            ("view_all", "Can view all data"),
            ("manage_school", "Can manage school-related settings and users"),
        ]


# 2. Admin Profile
class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="admin_profile")
    hire_date = models.DateField()
    
    class Meta:
        permissions = [
            ("manage_staff", "Can manage staff members"),
            ("manage_teachers", "Can manage teachers and their settings"),
        ]


# 3. Staff Profile with Permissions
class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="staff_profile")
    hire_date = models.DateField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    class Meta:
        permissions = [
            ("manage_students", "Can manage student profiles and data"),
            ("manage_classes", "Can manage classes and class-related settings"),
            ("manage_fees", "Can manage fee payments and related information"),
        ]


# 4. Teacher Profile and Class Association
class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_profile")
    hire_date = models.DateField()
    main_subject = models.CharField(max_length=100)
    
    class Meta:
        permissions = [
            ("manage_attendance", "Can manage attendance records"),
            ("manage_grades", "Can manage grades and exams"),
            ("manage_class_schedule", "Can manage class schedule and timetable"),
        ]


# 5. Class Model with Teacher and Student Relationships
class Class(models.Model):
    title = models.CharField(max_length=100)
    assigned_teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, related_name="assigned_classes")
    students = models.ManyToManyField('StudentProfile', related_name="classes")
    room_number = models.CharField(max_length=10)

    # Non-person entities associated with the class
    class_schedule = models.TextField()
    attendance_records = models.TextField(blank=True)  # Placeholder for detailed attendance model
    exams = models.TextField(blank=True)  # Placeholder for detailed exams model

    class Meta:
        permissions = [
            ("view_class_data", "Can view class-related information"),
        ]


# 6. Student Profile with Assigned Class and Grades
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    parent = models.ForeignKey('ParentProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name="children_students")
    enrollment_date = models.DateField()
    grade_level = models.CharField(max_length=20)

    class Meta:
        permissions = [
            ("view_class_schedule", "Can view class schedule"),
            ("view_grades", "Can view grades"),
        ]


# 7. Parent Profile with Child-Student Relationships
class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="parent_profile")
    children = models.ManyToManyField('StudentProfile', related_name="parents")

    class Meta:
        permissions = [
            ("view_child_progress", "Can view their child's progress and related data"),
        ]


# 8. Attendance Model Linked to Class and Students
class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendances")
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))


# 9. Exam Model Linked to Class and Students
class Exam(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="exams")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="exams")
    date = models.DateField()
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)


# 10. Fee Management Model for Students
class Fee(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="fees")
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
