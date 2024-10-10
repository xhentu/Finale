from django.contrib import admin

# Register your models here.
from .models import (
    CustomUser,
    AdminProfile,
    StaffProfile,
    TeacherProfile,
    StudentProfile,
    ParentProfile,
    Subject,
    Class,
    Schedule,
    Attendance,
    Exam,
    Grade,
    Fee,
)

# CustomUser admin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role',)

# BaseProfile Admin
class BaseProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hire_date')
    search_fields = ('user__username',)

# Admin Profile Admin
class AdminProfileAdmin(BaseProfileAdmin):
    pass

# Staff Profile Admin
class StaffProfileAdmin(BaseProfileAdmin):
    list_display = ('user', 'hire_date', 'position', 'department')

# Teacher Profile Admin
class TeacherProfileAdmin(BaseProfileAdmin):
    list_display = ('user', 'hire_date', 'main_subject')

# Student Profile Admin
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_instance', 'enrollment_date', 'grade_level')
    search_fields = ('user__username', 'class_instance__title')
    list_filter = ('class_instance',)

# Parent Profile Admin
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

# Class Admin
class ClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_teacher', 'room_number')
    search_fields = ('title', 'assigned_teacher__user__username')

# Subject Admin
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Schedule Admin
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('class_instance', 'section', 'day_of_week')
    search_fields = ('class_instance__title',)

# Attendance Admin
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_instance', 'date', 'status')
    search_fields = ('student__user__username', 'class_instance__title')
    list_filter = ('class_instance', 'status')

# Exam Admin
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'student', 'date', 'grade')
    search_fields = ('subject__name', 'student__user__username')
    list_filter = ('date',)

# Grade Admin
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'grade_value')
    search_fields = ('student__user__username', 'exam__subject__name')

# Fee Admin
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_due', 'due_date', 'paid')
    search_fields = ('student__user__username',)
    list_filter = ('paid',)

# Register models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AdminProfile, AdminProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(ParentProfile, ParentProfileAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Fee, FeeAdmin)
