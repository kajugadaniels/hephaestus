import os
import random
from datetime import date
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField

User = get_user_model()

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