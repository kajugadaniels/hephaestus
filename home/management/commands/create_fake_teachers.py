import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from django.core.files.base import ContentFile
from PIL import Image
import io
from django.utils import timezone
from home.models import Teacher

class Command(BaseCommand):
    help = 'Create fake teacher entries'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create 10 fake teachers
        for _ in range(10):
            name = fake.name()
            email = fake.email()
            phone_number = fake.phone_number()

            # Create the Teacher profile
            employee_id = f"T{fake.unique.random_number(digits=5)}"
            date_of_birth = fake.date_of_birth(minimum_age=25, maximum_age=65)
            gender = random.choice(['Male', 'Female'])
            nationality = fake.country()
            national_id = fake.unique.random_number(digits=10)
            marital_status = random.choice(['Single', 'Married', 'Divorced', 'Widowed'])
            alternative_phone_number = fake.phone_number()
            address = fake.address()
            position = fake.job()
            department = fake.random_element(elements=('Mathematics', 'Science', 'English', 'History', 'Art'))
            employment_status = random.choice(['Full-time', 'Part-time', 'Contract', 'Temporary'])
            date_joined = fake.date_between(start_date='-10y', end_date='today')
            years_of_experience = fake.random_int(min=0, max=30)
            highest_degree = random.choice(['Bachelor', 'Master', 'PhD'])
            major = fake.random_element(elements=('Education', 'Mathematics', 'Physics', 'Literature', 'History'))
            institution = fake.country()
            graduation_year = fake.year()
            certifications = fake.sentence(nb_words=10)
            skills = fake.sentence(nb_words=8)
            subjects_taught = ', '.join(fake.random_elements(elements=('Math', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Geography'), length=random.randint(1, 3)))
            classes_assigned = ', '.join(fake.random_elements(elements=('Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5'), length=random.randint(1, 3)))
            emergency_contact_name = fake.name()
            emergency_contact_relationship = fake.random_element(elements=('Spouse', 'Parent', 'Sibling', 'Friend'))
            emergency_contact_phone = fake.phone_number()
            bio = fake.paragraph()
            achievements = fake.paragraph()

            # Generate a fake image for the teacher
            img_byte_arr = io.BytesIO()
            image = Image.new('RGB', (720, 720), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            teacher = Teacher(
                name=name,
                email=email,
                phone_number=phone_number,
                employee_id=employee_id,
                date_of_birth=date_of_birth,
                gender=gender,
                nationality=nationality,
                national_id=national_id,
                marital_status=marital_status,
                alternative_phone_number=alternative_phone_number,
                address=address,
                position=position,
                department=department,
                employment_status=employment_status,
                date_joined=date_joined,
                years_of_experience=years_of_experience,
                highest_degree=highest_degree,
                major=major,
                institution=institution,
                graduation_year=graduation_year,
                certifications=certifications,
                skills=skills,
                subjects_taught=subjects_taught,
                classes_assigned=classes_assigned,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_relationship=emergency_contact_relationship,
                emergency_contact_phone=emergency_contact_phone,
                bio=bio,
                achievements=achievements,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            teacher.save()

            # Save the image
            teacher.image.save(f'teacher_{slugify(name)}_{date_of_birth}_{gender}.jpeg', ContentFile(img_byte_arr))

        self.stdout.write(self.style.SUCCESS('Successfully created 10 fake teachers'))
