from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom manager for user creation
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)

# Custom user model inheriting from AbstractUser
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, "Admin"),
        (2, "Staff"),
        (3, "Teacher"),
        (4, "Student"),
        (5, "Parent"),
    )
    
    # Removing username and using email as the login field
    username = None
    email = models.EmailField(unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")], default='M')
    profile_pic = models.ImageField(upload_to='profiles/', blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # Avoid reverse accessor clashes by adding related_name to groups and permissions
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"

class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey('Session', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.get_full_name()

class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminProfile.objects.create(user=instance)
        elif instance.user_type == 2:
            StaffProfile.objects.create(user=instance)
        elif instance.user_type == 3:
            TeacherProfile.objects.create(user=instance)
        elif instance.user_type == 4:
            StudentProfile.objects.create(user=instance)
        elif instance.user_type == 5:
            ParentProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminprofile.save()
    elif instance.user_type == 2:
        instance.staffprofile.save()
    elif instance.user_type == 3:
        instance.teacherprofile.save()
    elif instance.user_type == 4:
        instance.studentprofile.save()
    elif instance.user_type == 5:
        instance.parentprofile.save()

class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return f"{self.start_year} to {self.end_year}"

class Course(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Staff(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name

class Subject(models.Model):
    name = models.CharField(max_length=120)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE,)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
