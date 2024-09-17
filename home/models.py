import os
import random
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from imagekit.models import ProcessedImageField
from django.core.exceptions import ValidationError

User = get_user_model()

class AcademicYear(models.Model):
    name = models.CharField(max_length=9, unique=True, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='academic_years_created', null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='academic_years_updated', null=True, blank=True)
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date.")

def teacher_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'teachers/teacher_{slugify(instance.name)}_{instance.employee_id}_{instance.phone_number}{file_extension}'

class Teacher(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    MARITAL_STATUS_CHOICES = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    )

    EMPLOYMENT_STATUS_CHOICES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Temporary', 'Temporary'),
    )

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    image = ProcessedImageField(
        upload_to=teacher_image_path,
        processors=[ResizeToFill(720, 720)],
        format='JPEG',
        options={'quality': 90},
        null=True, blank=True
    )

    # Personal Information
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)

    # Contact Information
    alternative_phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(null=True, blank=True)

    # Professional Information
    position = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, null=True, blank=True)
    date_joined = models.DateField(null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)

    # Qualifications
    highest_degree = models.CharField(max_length=100, null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=200, null=True, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)

    # Additional Qualifications
    certifications = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)

    # Teaching Information
    subjects_taught = models.TextField(null=True, blank=True)
    classes_assigned = models.TextField(null=True, blank=True)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)

    # Additional Information
    bio = models.TextField(null=True, blank=True)
    achievements = models.TextField(null=True, blank=True)

    # System Fields
    delete_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='teachers_created')
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='teachers_updated')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['national_id']),
        ]

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def delete(self, *args, **kwargs):
        self.delete_status = True
        self.save()

def student_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'students/student_{slugify(instance.name)}_{instance.dob}_{instance.gender}{file_extension}'

def generate_unique_roll_id():
    while True:
        roll_id = str(random.randint(100000, 999999))
        if not Student.objects.filter(roll_id=roll_id).exists():
            return roll_id

class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    STUDENT_CURRENT_STATUS = (
        ('Active', 'Active'),
        ('Graduated', 'Graduated'),
        ('Transferred', 'Transferred'),
        ('Dropped', 'Dropped')
    )

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    roll_id = models.CharField(max_length=6, unique=True, editable=False, null=True, blank=True)
    image = ProcessedImageField(
        upload_to=student_image_path,
        processors=[ResizeToFill(720, 720)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True
    )
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    current_status = models.CharField(max_length=20, choices=STUDENT_CURRENT_STATUS, default='Active', null=True, blank=True)
    nationality = models.CharField(max_length=40, null=True, blank=True)

    # Contact Info
    cell = models.CharField(max_length=50, null=True, blank=True)
    village = models.CharField(max_length=50, null=True, blank=True)
    sector = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)

    # Emergency Contact Information
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)

    # Additional Information
    medical_conditions = models.TextField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    special_needs = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    # Audit fields
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    delete_status = models.BooleanField(default=False)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def age(self):
        today = timezone.now().date()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    
    def save(self, *args, **kwargs):
        if not self.roll_id:
            self.roll_id = generate_unique_roll_id()

        if self.pk is None:
            self.slug = slugify(self.name)
        else:
            original = Student.objects.get(pk=self.pk)
            if original.name != self.name:
                self.slug = slugify(self.name)
        
        super(Student, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_status = True
        self.save()

    def __str__(self):
        return self.name

@receiver(post_save, sender=Student)
def update_class_on_student_change(sender, instance, **kwargs):
    if instance.delete_status or instance.current_status != 'Active':
        for class_obj in instance.classes.all():
            class_obj.students.remove(instance)
            class_obj.capacity = class_obj.students.count()
            class_obj.save()

class Term(models.Model):
    TERM_CHOICES = [
        ('1', 'First Term'),
        ('2', 'Middle Term'),
        ('3', 'Final Term'),
    ]

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='terms', null=True, blank=True)
    name = models.CharField(max_length=1, choices=TERM_CHOICES, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='terms_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='terms_updated')
    delete_status = models.BooleanField(default=False)

    class Meta:
        unique_together = ['academic_year', 'name']
        ordering = ['academic_year', 'name']

    def __str__(self):
        return f"{self.get_name_display()} - {self.academic_year}"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date.")
        if self.start_date < self.academic_year.start_date or self.end_date > self.academic_year.end_date:
            raise ValidationError("Term dates must be within the academic year.")

class Class(models.Model):
    GRADE_CHOICES = [
        ('1', 'Year 1'),
        ('2', 'Year 2'),
        ('3', 'Year 3'),
        ('4', 'Year 4'),
        ('5', 'Year 5'),
        ('6', 'Year 6'),
    ]
    
    SECTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True, related_name='classes')
    name = models.CharField(max_length=50, null=True, blank=True)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, null=True, blank=True)
    head_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_classes')
    students = models.ManyToManyField('Student', related_name='classes', null=True, blank=True)
    capacity = models.PositiveIntegerField(default=30, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='classes_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='classes_updated')
    delete_status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Classes"
        unique_together = ['grade', 'section', 'academic_year']

    def __str__(self):
        return f"Year {self.grade} Grade {self.section} - {self.academic_year}"

class Subject(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='subjects_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='subjects_updated')
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        acronym = ''.join(word[0].upper() for word in self.name.split() if word)
        number = ''.join(str(random.randint(0, 9)) for _ in range(4))
        code = f"{acronym}{number}"
        
        # Check if code already exists and regenerate if necessary
        while Subject.objects.filter(code=code).exists():
            number = ''.join(str(random.randint(0, 9)) for _ in range(4))
            code = f"{acronym}{number}"
        
        return code

class ClassSubject(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='class_subjects', null=True, blank=True)
    class_group = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='class_subjects', null=True, blank=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='class_subjects', null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, related_name='taught_subjects', null=True, blank=True)
    day = models.CharField(max_length=10, choices=DAY_CHOICES, null=True, blank=True)
    starting_hour = models.TimeField(null=True, blank=True)
    ending_hour = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_subjects_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_subjects_updated')
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_group} - {self.subject} - {self.day}"

    def clean(self):
        break_start = timezone.datetime.strptime("10:15", "%H:%M").time()
        break_end = timezone.datetime.strptime("11:00", "%H:%M").time()
        lunch_start = timezone.datetime.strptime("12:30", "%H:%M").time()
        lunch_end = timezone.datetime.strptime("14:00", "%H:%M").time()

        if (break_start <= self.starting_hour < break_end) or (break_start < self.ending_hour <= break_end) or \
           (self.starting_hour < break_start and self.ending_hour > break_end):
            raise ValidationError({
                "starting_hour": f"Class time ({self.starting_hour.strftime('%H:%M')} - {self.ending_hour.strftime('%H:%M')}) overlaps with break time (10:15 - 11:00).",
                "ending_hour": f"Class time ({self.starting_hour.strftime('%H:%M')} - {self.ending_hour.strftime('%H:%M')}) overlaps with break time (10:15 - 11:00)."
            })
        elif (lunch_start <= self.starting_hour < lunch_end) or (lunch_start < self.ending_hour <= lunch_end) or \
             (self.starting_hour < lunch_start and self.ending_hour > lunch_end):
            raise ValidationError({
                "starting_hour": f"Class time ({self.starting_hour.strftime('%H:%M')} - {self.ending_hour.strftime('%H:%M')}) overlaps with lunch time (12:30 - 14:00).",
                "ending_hour": f"Class time ({self.starting_hour.strftime('%H:%M')} - {self.ending_hour.strftime('%H:%M')}) overlaps with lunch time (12:30 - 14:00)."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True, choices=ATTENDANCE_CHOICES)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='attendances_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='attendances_updated')

    class Meta:
        unique_together = ('student', 'class_subject', 'date')

    def clean(self):
        if self.date.weekday() > 4:
            raise ValidationError("Attendance can only be marked for weekdays (Monday to Friday).")
        
        if Holiday.objects.filter(date=self.date).exists():
            raise ValidationError("Attendance cannot be marked for a holiday.")

        if not (self.class_subject.term.start_date <= self.date <= self.class_subject.term.end_date):
            raise ValidationError("Attendance date must be within the term dates.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.class_subject.subject.name} - {self.date}"

class Holiday(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='holidays', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='holidays_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='holidays_updated')

    def __str__(self):
        return f"{self.name} - {self.date}"

    class Meta:
        ordering = ['date']