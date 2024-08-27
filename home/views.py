from home.forms import *
from home.models import *
from account.models import *
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Exists, OuterRef
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
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            
            # Handle image upload separately
            if 'image' in request.FILES:
                student.image = request.FILES['image']
            
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

@login_required
def getTeachers(request):
    teachers = Teacher.objects.filter(delete_status=False).order_by('-created_at')
    return render(request, 'pages/teachers/index.html', {'teachers': teachers})

@login_required
def addTeacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user = request.user
            teacher.created_by = request.user
            teacher.save()
            messages.success(request, 'Teacher added successfully.')
            return redirect('home:getTeachers')
    else:
        form = TeacherForm()
    return render(request, 'pages/teachers/create.html', {'form': form})

@login_required
def viewTeacher(request, employee_id):
    teacher = get_object_or_404(Teacher, employee_id=employee_id, delete_status=False)
    return render(request, 'pages/teachers/show.html', {'teacher': teacher})

@login_required
def editTeacher(request, employee_id):
    teacher = get_object_or_404(Teacher, employee_id=employee_id, delete_status=False)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.updated_by = request.user
            teacher.save()
            messages.success(request, 'Teacher updated successfully.')
            return redirect('home:viewTeacher', employee_id=teacher.employee_id)
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'pages/teachers/edit.html', {'form': form, 'teacher': teacher})

@login_required
def deleteTeacher(request, employee_id):
    teacher = get_object_or_404(Teacher, employee_id=employee_id, delete_status=False)
    teacher.delete_status = True
    teacher.updated_by = request.user
    teacher.save()
    messages.success(request, 'Teacher deleted successfully.')
    return redirect('home:getTeachers')

@login_required
def getTerms(request):
    terms = Term.objects.filter(delete_status=False).order_by('-created_at')

    context = {
        'terms': terms
    }

    return render(request, 'pages/terms/index.html', context)

@login_required
def addTerm(request):
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            term = form.save(commit=False)
            term.created_by = request.user
            term.save()
            messages.success(request, 'Term added successfully.')
            return redirect('home:getTerms')
    else:
        form = TermForm()

    context = {
        'form': form
    }

    return render(request, 'pages/terms/create.html', context)

@login_required
def viewTerm(request, id):
    term = get_object_or_404(Term, id=id, delete_status=False)

    context = {
        'term': term
    }

    return render(request, 'pages/terms/show.html', context)

@login_required
def editTerm(request, id):
    term = get_object_or_404(Term, id=id, delete_status=False)
    if request.method == 'POST':
        form = TermForm(request.POST, instance=term)
        if form.is_valid():
            term = form.save(commit=False)
            term.updated_by = request.user
            term.save()
            messages.success(request, 'Term updated successfully.')
            return redirect('home:viewTerm', id=term.id)
    else:
        form = TermForm(instance=term)

    context = {
        'form': form,
        'term': term
    }

    return render(request, 'pages/terms/edit.html', context)

@login_required
def deleteTerm(request, id):
    term = get_object_or_404(Term, id=id, delete_status=False)
    term.delete_status = True
    term.updated_by = request.user
    term.save()
    messages.success(request, 'Term deleted successfully.')
    return redirect('home:getTerms')

@login_required
def getAcademicYears(request):
    academic_years = AcademicYear.objects.filter(delete_status=False)

    context = {
        'academic_years': academic_years
    }

    return render(request, 'pages/academicYears/index.html', context)

@login_required
def addAcademicYear(request):
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            academic_year = form.save(commit=False)
            academic_year.created_by = request.user
            academic_year.save()
            messages.success(request, 'Academic Year added successfully.')
            return redirect('home:getAcademicYears')
    else:
        form = AcademicYearForm()

    context = {
        'form': form
    }

    return render(request, 'pages/academicYears/create.html', context)

@login_required
def viewAcademicYear(request, id):
    academic_year = get_object_or_404(AcademicYear, id=id, delete_status=False)
    classes = Class.objects.filter(academic_year=academic_year, delete_status=False)

    context = {
        'academic_year': academic_year,
        'classes': classes,
    }

    return render(request, 'pages/academicYears/show.html', context)

@login_required
def editAcademicYear(request, id):
    academic_year = get_object_or_404(AcademicYear, id=id, delete_status=False)
    if request.method == 'POST':
        form = AcademicYearForm(request.POST, instance=academic_year)
        if form.is_valid():
            academic_year = form.save(commit=False)
            academic_year.updated_by = request.user
            academic_year.save()
            messages.success(request, 'Academic Year updated successfully.')
            return redirect('home:viewAcademicYear', id=academic_year.id)
    else:
        form = AcademicYearForm(instance=academic_year)

    context = {
        'form': form,
        'academic_year': academic_year
    }

    return render(request, 'pages/academicYears/edit.html', context)

@login_required
def deleteAcademicYear(request, id):
    academic_year = get_object_or_404(AcademicYear, id=id, delete_status=False)
    academic_year.delete_status = True
    academic_year.updated_by = request.user
    academic_year.save()
    messages.success(request, 'Academic Year deleted successfully.')
    return redirect('home:getAcademicYears')

@login_required
def getClasses(request):
    classes = Class.objects.filter(delete_status=False)

    context = {
        'classes': classes
    }

    return render(request, 'pages/classes/index.html', context)

@login_required
def addClass(request, academic_year_id):
    academic_year = get_object_or_404(AcademicYear, id=academic_year_id)
    
    if request.method == 'POST':
        form = ClassForm(request.POST)
        try:
            if form.is_valid():
                class_obj = form.save(commit=False)
                class_obj.created_by = request.user
                class_obj.academic_year = academic_year
                class_obj.save()
                
                # Handle students separately
                student_ids = request.POST.getlist('students')
                
                # Filter students who are not already in a class for this academic year
                available_students = Student.objects.filter(
                    id__in=student_ids,
                    delete_status=False,
                    current_status='Active'
                ).exclude(
                    Exists(
                        Class.objects.filter(
                            academic_year=academic_year,
                            students=OuterRef('pk')
                        )
                    )
                )
                
                class_obj.students.set(available_students)
                
                # Set capacity to the number of selected students
                class_obj.capacity = available_students.count()
                class_obj.save()
                
                if available_students.count() < len(student_ids):
                    messages.warning(request, 'Some students were not added as they are already assigned to a class in this academic year.')
                
                messages.success(request, 'Class added successfully.')
                return redirect('home:getClasses')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except IntegrityError:
            messages.error(request, 'A class with the same grade, section, and academic year already exists.')
        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
    else:
        form = ClassForm(initial={'academic_year': academic_year})
    
    # Fetch students not assigned to any class in the current academic year
    students = Student.objects.filter(
        delete_status=False,
        current_status='Active'
    ).exclude(
        Exists(
            Class.objects.filter(
                academic_year=academic_year,
                students=OuterRef('pk')
            )
        )
    ).order_by('-created_at')
    
    headTeachers = Teacher.objects.filter(delete_status=False).order_by('-created_at')
    
    context = {
        'form': form,
        'students': students,
        'headTeachers': headTeachers,
        'academic_year': academic_year,
    }

    return render(request, 'pages/classes/create.html', context)

@login_required
def viewClass(request, id):
    class_obj = get_object_or_404(Class, id=id, delete_status=False)
    active_students = class_obj.students.filter(delete_status=False, current_status='Active')

    context = {
        'class': class_obj,
        'active_students': active_students
    }

    return render(request, 'pages/classes/show.html', context)

@login_required
def editClass(request, id):
    class_obj = get_object_or_404(Class, id=id, delete_status=False)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            class_obj = form.save(commit=False)
            class_obj.updated_by = request.user
            class_obj.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Class updated successfully.')
            return redirect('home:viewClass', id=class_obj.id)
    else:
        form = ClassForm(instance=class_obj)

    context = {
        'form': form,
        'class': class_obj
    }

    return render(request, 'pages/classes/edit.html', context)

@login_required
def deleteClass(request, id):
    class_obj = get_object_or_404(Class, id=id, delete_status=False)
    class_obj.delete_status = True
    class_obj.updated_by = request.user
    class_obj.save()
    messages.success(request, 'Class deleted successfully.')
    return redirect('home:getClasses')