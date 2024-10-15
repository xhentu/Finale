from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import AdminProfile, StaffProfile, TeacherProfile, StudentProfile, ParentProfile, CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign role-based profile creation
            role = request.POST.get('role')  # Ensure role is captured from form input
            user.role = role  # Set the role from the form
            user.save()

            # Check if the profile already exists before creating a new one
            if role == 'admin':
                if not AdminProfile.objects.filter(user=user).exists():
                    AdminProfile.objects.create(user=user)
            elif role == 'staff':
                if not StaffProfile.objects.filter(user=user).exists():
                    StaffProfile.objects.create(user=user)
            elif role == 'teacher':
                if not TeacherProfile.objects.filter(user=user).exists():
                    TeacherProfile.objects.create(user=user)
            elif role == 'student':
                if not StudentProfile.objects.filter(user=user).exists():
                    StudentProfile.objects.create(user=user)
            elif role == 'parent':
                if not ParentProfile.objects.filter(user=user).exists():
                    ParentProfile.objects.create(user=user)

            return redirect('success')  # Redirect to login after registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def check_permissions(request):
    # Replace 'username' with the actual username of the user you want to test
    username = 'fourthuser'  # example username
    try:
        user = CustomUser.objects.get(username=username)
        permissions = user.get_all_permissions()

        # Print the permissions to the terminal
        print(f'Permissions for {username}:')
        if permissions:
            for perm in permissions:
                print(perm)
        else:
            print('No permissions found for this user.')

    except CustomUser.DoesNotExist:
        print('User does not exist.')
