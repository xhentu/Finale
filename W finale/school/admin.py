from django.contrib import admin
from .models import CustomUser, AdminProfile, StaffProfile, TeacherProfile, StudentProfile, ParentProfile
from django.contrib.auth.admin import UserAdmin

# Register the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff']
    fieldsets = UserAdmin.fieldsets

# Register each Profile model in the admin interface
admin.site.register(AdminProfile)
admin.site.register(StaffProfile)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(ParentProfile)
