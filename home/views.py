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
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home:dashboard')

    getUsers = User.objects.all().order_by('-created_at')

    context = {
        'getUsers': getUsers
    }

    return render(request, 'pages/users/index.html', context)

@login_required
def addUser(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home:dashboard')

    roles = ['Admin', 'Director', 'Teacher', 'Student'] if request.user.role == 'Admin' or request.user.is_superuser else ['Director']

    if request.method == 'POST':
        form = UserCreationForm(request.POST, roles=roles)

        # Check if form is valid first
        if form.is_valid():
            required_fields = ['name', 'email', 'phone_number', 'password', 'role']
            missing_fields = [field for field in required_fields if not form.cleaned_data.get(field)]

            if missing_fields:
                messages.error(request, f"{', '.join([field.replace('_', ' ').capitalize() for field in missing_fields])} {'is' if len(missing_fields) == 1 else 'are'} required.")
            elif form.cleaned_data.get("password") != form.cleaned_data.get("password_confirmation"):
                messages.error(request, "Password does not match.")
            elif form.cleaned_data.get("role") not in roles:
                messages.error(request, "Invalid role selected.")
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.added_by = request.user
                user.save()
                messages.success(request, "User successfully added.")
                return redirect('home:getUsers')
        else:
            # Display form errors
            for error in form.errors.values():
                messages.error(request, error)

    else:
        form = UserCreationForm(roles=roles)

    context = {
        'form': form,
        'logged_in_user': request.user
    }

    return render(request, 'pages/users/create.html', context)

@login_required
def getStudents(request):
    return render(request, 'pages/students/index.html')

@login_required
def addStudent(request):
    return render(request, 'pages/students/create.html')