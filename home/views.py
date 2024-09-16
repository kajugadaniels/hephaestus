from home.forms import *
from home.models import *
from datetime import time
from account.models import *
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
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

    context = {
        'teachers': teachers
    }
    return render(request, 'pages/teachers/index.html', context)

@login_required
def addTeacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.created_by = request.user
            teacher.save()
            messages.success(request, 'Teacher added successfully.')
            return redirect('home:getTeachers')
    else:
        form = TeacherForm()

    context = {
        'form': form
    }
    return render(request, 'pages/teachers/create.html', context)

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
@login_required
def getAcademicYears(request):
    academic_years = AcademicYear.objects.filter(delete_status=False).order_by('-created_at')
    today = timezone.now().date()

    for year in academic_years:
        if year.start_date and year.end_date:
            if today < year.start_date:
                year.status = "Not Started"
            elif year.start_date <= today <= year.end_date:
                year.status = "Ongoing"
            else:
                year.status = "Finished"
        else:
            year.status = "Dates not set"

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
        try:
            if form.is_valid():
                updated_class = form.save(commit=False)
                updated_class.updated_by = request.user
                updated_class.save()
                
                # Handle students separately
                student_ids = request.POST.getlist('students')
                available_students = Student.objects.filter(
                    id__in=student_ids,
                    delete_status=False,
                    current_status='Active'
                ).exclude(
                    Exists(
                        Class.objects.filter(
                            academic_year=class_obj.academic_year,
                            students=OuterRef('pk')
                        ).exclude(pk=class_obj.pk)
                    )
                )
                
                updated_class.students.set(available_students)
                updated_class.capacity = available_students.count()
                updated_class.save()
                
                messages.success(request, 'Class updated successfully.')
                return redirect('home:viewClass', id=updated_class.id)
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
        form = ClassForm(instance=class_obj)
    
    # Fetch students not assigned to any class in the current academic year (excluding this class)
    students = Student.objects.filter(
        delete_status=False,
        current_status='Active'
    ).exclude(
        Exists(
            Class.objects.filter(
                academic_year=class_obj.academic_year,
                students=OuterRef('pk')
            ).exclude(pk=class_obj.pk)
        )
    )
    
    # Add currently assigned students to the queryset
    students = students.union(class_obj.students.all())
    
    headTeachers = Teacher.objects.filter(delete_status=False).order_by('-created_at')
    
    context = {
        'form': form,
        'class': class_obj,
        'students': students,
        'headTeachers': headTeachers,
        'academic_year': class_obj.academic_year,
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

@login_required
def getSubjects(request):
    subjects = Subject.objects.filter(delete_status=False).order_by('-created_at')

    context = {
        'subjects': subjects
    }

    return render(request, 'pages/subjects/index.html', context)

@login_required
def addSubject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.created_by = request.user
            subject.save()
            messages.success(request, 'Subject added successfully.')
            return redirect('home:getSubjects')
    else:
        form = SubjectForm()

    context = {
        'form': form
    }

    return render(request, 'pages/subjects/create.html', context)

@login_required
def viewSubject(request, id):
    subject = get_object_or_404(Subject, id=id, delete_status=False)

    context = {
        'subject': subject
    }

    return render(request, 'pages/subjects/show.html', context)

@login_required
def editSubject(request, id):
    subject = get_object_or_404(Subject, id=id, delete_status=False)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.updated_by = request.user
            subject.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('home:viewSubject', id=subject.id)
    else:
        form = SubjectForm(instance=subject)

    context = {
        'form': form,
        'subject': subject
    }

    return render(request, 'pages/subjects/edit.html', context)

@login_required
def deleteSubject(request, id):
    subject = get_object_or_404(Subject, id=id, delete_status=False)
    subject.delete_status = True
    subject.updated_by = request.user
    subject.save()
    messages.success(request, 'Subject deleted successfully.')
    return redirect('home:getSubjects')

@login_required
def assignSubjects(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id, delete_status=False)
    if request.method == 'POST':
        try:
            subjects = request.POST.getlist('subjects[]')
            teachers = request.POST.getlist('teachers[]')
            days = request.POST.getlist('days[]')
            starting_hours = request.POST.getlist('starting_hours[]')
            ending_hours = request.POST.getlist('ending_hours[]')

            if len(subjects) != len(teachers) or len(subjects) != len(days) or len(subjects) != len(starting_hours) or len(subjects) != len(ending_hours):
                raise ValueError("Mismatched data lengths")

            for i in range(len(subjects)):
                try:
                    class_subject = ClassSubject(
                        class_group=class_obj,
                        subject_id=subjects[i],
                        teacher_id=teachers[i],
                        day=days[i],
                        starting_hour=starting_hours[i],
                        ending_hour=ending_hours[i],
                        created_by=request.user
                    )
                    class_subject.full_clean()
                    class_subject.save()
                except ValidationError as e:
                    for field, errors in e.message_dict.items():
                        for error in errors:
                            messages.error(request, f"{error}")
                    return redirect('home:assignSubjects', class_id=class_id)

            messages.success(request, 'Subjects assigned successfully.')
            return redirect('home:getClassSubjects', class_id=class_id)
        except ValueError as e:
            messages.error(request, f'Error: Invalid data format. {str(e)}')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
    
    subjects = Subject.objects.filter(delete_status=False)
    teachers = Teacher.objects.filter(delete_status=False)

    context = {
        'class': class_obj,
        'subjects': subjects,
        'teachers': teachers
    }

    return render(request, 'pages/class-subject/create.html', context)

@login_required
def getClassSubjects(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id, delete_status=False)
    class_subjects = ClassSubject.objects.filter(class_group=class_obj, delete_status=False).order_by('day', 'starting_hour')
    
    # Define break and lunch times
    break_time = {'name': 'Break Time', 'starting_hour': time(10, 15), 'ending_hour': time(11, 0)}
    lunch_time = {'name': 'Lunch Time', 'starting_hour': time(12, 30), 'ending_hour': time(14, 0)}
    
    # Group subjects by day
    subjects_by_day = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
    }
    
    for subject in class_subjects:
        day_schedule = subjects_by_day[subject.day]
        day_schedule.append({
            'name': subject.subject.name,
            'teacher': subject.teacher,
            'starting_hour': subject.starting_hour,
            'ending_hour': subject.ending_hour,
            'is_break': False,
            'id': subject.id
        })
    
    # Add break and lunch times to each day
    for day_schedule in subjects_by_day.values():
        if not any(s['name'] == 'Break Time' for s in day_schedule):
            day_schedule.append({**break_time, 'is_break': True, 'teacher': None, 'id': None})
        if not any(s['name'] == 'Lunch Time' for s in day_schedule):
            day_schedule.append({**lunch_time, 'is_break': True, 'teacher': None, 'id': None})
        
        # Sort the day's schedule
        day_schedule.sort(key=lambda x: x['starting_hour'])
    
    context = {
        'class': class_obj,
        'subjects_by_day': subjects_by_day,
    }
    
    return render(request, 'pages/class-subject/index.html', context)

@login_required
def editClassSubject(request, id):
    class_subject = get_object_or_404(ClassSubject, id=id, delete_status=False)
    
    if request.method == 'POST':
        form = ClassSubjectForm(request.POST, instance=class_subject)
        if form.is_valid():
            try:
                updated_class_subject = form.save(commit=False)
                updated_class_subject.updated_by = request.user
                updated_class_subject.full_clean()
                updated_class_subject.save()
                messages.success(request, 'Class subject updated successfully.')
                return redirect('home:getClassSubjects', class_id=class_subject.class_group.id)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{error}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = ClassSubjectForm(instance=class_subject)
    
    context = {
        'form': form,
        'class_subject': class_subject
    }

    return render(request, 'pages/class-subject/edit.html', context)

@login_required
def deleteClassSubject(request, id):
    class_subject = get_object_or_404(ClassSubject, id=id, delete_status=False)
    class_subject.delete_status = True
    class_subject.save()
    messages.success(request, 'Class subject deleted successfully.')
    return redirect('home:getClassSubjects', class_id=class_subject.class_group.id)