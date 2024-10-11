from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. CustomUser Model
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
    def __str__(self):
        return f"{self.username} ({self.role})"

# 2. Base Profile for common fields
class BaseProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="%(class)s_profile")
    hire_date = models.DateField()

    class Meta:
        abstract = True

# 3. Admin Profile
class AdminProfile(BaseProfile):
    pass

# 4. Staff Profile
class StaffProfile(BaseProfile):
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.user.username} - {self.position} ({self.department})"

# 5. Teacher Profile
class TeacherProfile(BaseProfile):
    main_subject = models.CharField(max_length=100)
    additional_subjects = models.ManyToManyField('Subject', blank=True, related_name='additional_teachers')
    def __str__(self):
        return f"{self.user.username} - {self.main_subject}"

# 6. Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

# 7. Class Model
class Class(models.Model):
    title = models.CharField(max_length=100)
    assigned_teacher = models.ForeignKey('TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_classes")  # Optional
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name="classes")
    room_number = models.CharField(max_length=10)

    def assign_teacher(self, teacher):
        """Assign teacher to class after creation."""
        self.assigned_teacher = teacher
        self.save()

    def __str__(self):
        assigned_teacher_str = self.assigned_teacher.user.username if self.assigned_teacher else "Not assigned"
        return f"{self.title} ({self.subject.name}) - Teacher: {assigned_teacher_str}"

# 8. Schedule Model
class Schedule(models.Model):
    SECTION_CHOICES = [
        ('1st Section', '9:00 am - 10:30 am'),
        ('2nd Section', '10:45 am - 12:15 pm'),
        ('3rd Section', '12:45 pm - 1:15 pm'),
        ('4th Section', '2:00 pm - 3:30 pm'),
    ]
    class_instance = models.ForeignKey('Class', on_delete=models.CASCADE, related_name="timetable", null=True, blank=True)  # Optional
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

    def __str__(self):
        return f"schedule for {self.class_instance.title}"
    
# 9. Student Profile
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    class_instance = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True, related_name="enrolled_students")  # Optional
    parent = models.ForeignKey('ParentProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name="children_students")
    enrollment_date = models.DateField()
    grade_level = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.user.username} - {self.grade_level}"

# 10. Parent Profile
class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="parent_profile")
    children = models.ManyToManyField('StudentProfile', related_name="parents", blank=True)

    def __str__(self):
  # You can modify this to display children names if needed
        return f"{self.user.username} - parent of {self.children}"

# 11. Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name="attendances")
    class_instance = models.ForeignKey('Class', on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))

    def __str__(self):
        return f"{self.student.user.username} - {self.class_instance.title} ({self.date}): {self.status}"

# 12. Exam Model
class Exam(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name="exams")
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name="exams")
    date = models.DateField()
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('subject', 'student', 'date')

    def __str__(self):
        return f"{self.subject.name} Exam - {self.student.user.username} ({self.date})"

# 13. Grade Model
class Grade(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name="grades")
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, related_name="grades")
    grade_value = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)
    def __str__(self):
        return f"{self.exam.subject.name} Exam - {self.student.user.username} ({self.grade_value})"
# 14. Fee Model
class Fee(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name="fees")
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(db_index=True)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        payment_status = "Paid" if self.paid else "Unpaid"
        return f"Fee for {self.student.user.username} - Amount: {self.amount_due} ({payment_status})"