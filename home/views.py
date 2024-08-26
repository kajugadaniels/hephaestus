from home.forms import *
from home.models import *
from account.models import *
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

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

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        path = default_storage.save(f'quill_images/{image.name}', image)
        return JsonResponse({'location': f'{settings.MEDIA_URL}{path}'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def getStudents(request):
    students = Student.objects.filter(delete_status=False).order_by('-created_at')

    context = {
        'students': students
    }

    return render(request, 'pages/students/index.html', context)

@login_required
def addStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.modified_by = request.user
            student.save()
            messages.success(request, 'Student added successfully.')
            return redirect('home:getStudents')
    else:
        form = StudentForm()

    context = {
        'form': form
    }

    return render(request, 'pages/students/create.html', context)

@login_required
def viewStudent(request, slug):
    student = get_object_or_404(Student, slug=slug, delete_status=False)

    context = {
        'student': student
    }

    return render(request, 'pages/students/show.html', context)

@login_required
def editStudent(request, slug):
    student = get_object_or_404(Student, slug=slug, delete_status=False)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.modified_by = request.user
            student.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('home:viewStudent', slug=student.slug)
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'student': student
    }

    return render(request, 'pages/students/edit.html', context)

@login_required
def deleteStudent(request, slug):
    student = get_object_or_404(Student, slug=slug, delete_status=False)
    student.delete_status = True
    student.modified_by = request.user
    student.save()
    messages.success(request, 'Student deleted successfully.')
    return redirect('home:getStudents')