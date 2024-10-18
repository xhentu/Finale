# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import CustomUser, AdminProfile, StaffProfile, TeacherProfile, StudentProfile, ParentProfile

# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'admin':
#             AdminProfile.objects.create(user=instance)
#         elif instance.role == 'staff':
#             StaffProfile.objects.create(user=instance)
#         elif instance.role == 'teacher':
#             TeacherProfile.objects.create(user=instance)
#         elif instance.role == 'student':
#             StudentProfile.objects.create(user=instance)
#         elif instance.role == 'parent':
#             ParentProfile.objects.create(user=instance)
            
# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     # Check for the existence of profiles before saving
#     if hasattr(instance, 'staffprofile'):
#         instance.staffprofile.save()
#     if hasattr(instance, 'adminprofile'):
#         instance.adminprofile.save()
#     if hasattr(instance, 'teacherprofile'):
#         instance.teacherprofile.save()
#     if hasattr(instance, 'studentprofile'):
#         instance.studentprofile.save()
#     if hasattr(instance, 'parentprofile'):
#         instance.parentprofile.save()

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import Permission
# from .models import CustomUser, AdminProfile, StaffProfile, TeacherProfile, StudentProfile, ParentProfile

# # Define a dictionary to map roles to profile models
# ROLE_PROFILE_MAPPING = {
#     'admin': AdminProfile,
#     'staff': StaffProfile,
#     'teacher': TeacherProfile,
#     'student': StudentProfile,
#     'parent': ParentProfile,
# }

# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         print('we got signals')
#         profile_model = ROLE_PROFILE_MAPPING.get(instance.role)
#         if profile_model:
#             profile_model.objects.get_or_create(user=instance)
#         assign_permissions(instance)

# def assign_permissions(user):
#     print('assigning permissions')
#     """
#     Automatically assign permissions based on user roles.
#     For each role, add permissions according to their needs.
#     """
#     if user.role == 'admin':
#         user.is_staff = True  # Admins have staff permissions too
#         user.user_permissions.set(Permission.objects.all())  # Admins get all permissions
#     elif user.role == 'staff':
#         user.is_staff = True
#         # Add staff-specific permissions
#         staff_permissions = Permission.objects.filter(codename__in=['add_student', 'change_student', 'delete_student'])
#         user.user_permissions.set(staff_permissions)
#     elif user.role == 'teacher':
#         # Add teacher-specific permissions
#         teacher_permissions = Permission.objects.filter(codename__in=['view_student', 'add_grade', 'change_grade'])
#         user.user_permissions.set(teacher_permissions)
#     elif user.role == 'student':
#         # Students have minimal permissions
#         student_permissions = Permission.objects.filter(codename='view_grade')
#         user.user_permissions.set(student_permissions)
#     elif user.role == 'parent':
#         # Add parent-specific permissions
#         parent_permissions = Permission.objects.filter(codename='view_student')
#         user.user_permissions.set(parent_permissions)

#     user.save()  # Save the user after setting permissions

from django.contrib.auth.models import Permission, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, AdminProfile, StaffProfile, TeacherProfile, StudentProfile, ParentProfile


@receiver(post_save, sender=CustomUser)
def create_profile_and_assign_permissions(sender, instance, created, **kwargs):
    if created:
        print(f"User {instance.username} created with role {instance.role}")
        
        # Create profile based on role
        if instance.role == 'admin':
            AdminProfile.objects.create(user=instance)
            print(f"Admin profile created for {instance.username}")

            # Assign admin permissions (modify the codenames accordingly)
            admin_permissions = Permission.objects.filter(codename__in=[
                'add_staff', 'change_staff', 'view_staff', 'delete_staff',
                'add_student', 'change_student', 'view_student', 'delete_student'
            ])
            admin_group, group_created = Group.objects.get_or_create(name='Admin')
            if group_created:
                admin_group.permissions.add(*admin_permissions)
                print(f"Admin group created and permissions added")
            instance.groups.add(admin_group)
            print(f"{instance.username} added to Admin group")

        elif instance.role == 'staff':
            StaffProfile.objects.create(user=instance)
            print(f"Staff profile created for {instance.username}")

            # Assign staff permissions (modify the codenames accordingly)
            staff_permissions = Permission.objects.filter(codename__in=[
                'view_student', 'view_teacher', 'change_teacher'
            ])
            staff_group, group_created = Group.objects.get_or_create(name='Staff')
            if group_created:
                staff_group.permissions.add(*staff_permissions)
                print(f"Staff group created and permissions added")
            instance.groups.add(staff_group)
            print(f"{instance.username} added to Staff group")

        elif instance.role == 'teacher':
            TeacherProfile.objects.create(user=instance)
            print(f"Teacher profile created for {instance.username}")

            # Assign teacher permissions (modify the codenames accordingly)
            teacher_permissions = Permission.objects.filter(codename__in=[
                'add_student', 'change_student', 'view_student', 'delete_student'
            ])
            teacher_group, group_created = Group.objects.get_or_create(name='Teacher')
            if group_created:
                teacher_group.permissions.add(*teacher_permissions)
                print(f"Teacher group created and permissions added")
            instance.groups.add(teacher_group)
            print(f"{instance.username} added to Teacher group")

        elif instance.role == 'student':
            StudentProfile.objects.create(user=instance)
            print(f"Student profile created for {instance.username}")

            # Assign student permissions (modify the codenames accordingly)
            student_permissions = Permission.objects.filter(codename__in=[
                'view_timetable', 'view_grades'
            ])
            student_group, group_created = Group.objects.get_or_create(name='Student')
            if group_created:
                student_group.permissions.add(*student_permissions)
                print(f"Student group created and permissions added")
            instance.groups.add(student_group)
            print(f"{instance.username} added to Student group")

        elif instance.role == 'parent':
            ParentProfile.objects.create(user=instance)
            print(f"Parent profile created for {instance.username}")

            # Assign parent permissions (modify the codenames accordingly)
            parent_permissions = Permission.objects.filter(codename__in=[
                'view_student_performance', 'view_student_attendance'
            ])
            parent_group, group_created = Group.objects.get_or_create(name='Parent')
            if group_created:
                parent_group.permissions.add(*parent_permissions)
                print(f"Parent group created and permissions added")
            instance.groups.add(parent_group)
            print(f"{instance.username} added to Parent group")
