from account.models import *
from django.contrib import messages
from home.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')

@login_required
def getUsers(request):
    # if request.user.role == 'Admin':
    #     messages.error(request, "You are not authorized to access this page.")
    #     return redirect('home:dashboard')

    getUsers = User.objects.all().order_by('-created_at')

    context = {
        'getUsers': getUsers
    }

    return render(request, 'pages/users/index.html', context)

@login_required
def addUser(request):
    # Check if the user has permission to register new users
    if request.user.role not in ['Admin', 'Director']:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home:dashboard')

    # Define allowed roles based on the current user's role
    allowed_roles = User.ROLE_CHOICES if request.user.role == 'Admin' or request.user.is_superuser else [('Teacher', 'Teacher'), ('Student', 'Student')]

    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES, roles=allowed_roles)
        if form.is_valid():
            required_fields = ['name', 'email', 'phone_number', 'password', 'role']
            missing_fields = [field for field in required_fields if not form.cleaned_data.get(field)]
            
            if missing_fields:
                messages.error(request, f"{', '.join([field.replace('_', ' ').capitalize() for field in missing_fields])} {'is' if len(missing_fields) == 1 else 'are'} required.")
            elif form.cleaned_data.get("password") != form.cleaned_data.get("password_confirmation"):
                messages.error(request, "Passwords do not match.")
            elif form.cleaned_data.get("role") not in dict(allowed_roles):
                messages.error(request, "Invalid role selected.")
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.added_by = request.user
                user.save()
                messages.success(request, "User added successfully.")
                return redirect('home:getUsers')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm(roles=allowed_roles)

    context = {
        'form': form,
        'logged_in_user': request.user
    }

    return render(request, 'pages/users/create.html', context);