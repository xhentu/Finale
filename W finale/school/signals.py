from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, AdminProfile, StaffProfile, TeacherProfile, StudentProfile, ParentProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'admin':
            AdminProfile.objects.create(user=instance)
        elif instance.role == 'staff':
            StaffProfile.objects.create(user=instance)
        elif instance.role == 'teacher':
            TeacherProfile.objects.create(user=instance)
        elif instance.role == 'student':
            StudentProfile.objects.create(user=instance)
        elif instance.role == 'parent':
            ParentProfile.objects.create(user=instance)
            
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # Check for the existence of profiles before saving
    if hasattr(instance, 'staffprofile'):
        instance.staffprofile.save()
    if hasattr(instance, 'adminprofile'):
        instance.adminprofile.save()
    if hasattr(instance, 'teacherprofile'):
        instance.teacherprofile.save()
    if hasattr(instance, 'studentprofile'):
        instance.studentprofile.save()
    if hasattr(instance, 'parentprofile'):
        instance.parentprofile.save()
