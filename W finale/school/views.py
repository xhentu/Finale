from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@login_required
def create_user(request):
    if not request.user.is_superuser and request.user.role != 'admin':
        return redirect('home')  # Only allow superusers or admin to create users

    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('user_list')  # Redirect to the list of users (create this later)
    else:
        form = UserCreateForm()

    return render(request, 'school/create_user.html', {'form': form})
