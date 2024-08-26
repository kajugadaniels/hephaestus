import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from django.core.files.base import ContentFile
from PIL import Image
import io
from home.models import Student

class Command(BaseCommand):
    help = 'Create fake student entries'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create 30 fake students
        for _ in range(30):
            name = fake.name()
            dob = fake.date_of_birth(minimum_age=5, maximum_age=18)
            gender = random.choice(['Male', 'Female'])
            nationality = fake.country()
            current_status = random.choice(['Active', 'Graduated', 'Transferred', 'Dropped'])
            cell = fake.phone_number()
            village = fake.city_suffix()
            sector = fake.state()
            district = fake.state_abbr()
            emergency_contact_name = fake.name()
            emergency_contact_relation = fake.random_element(elements=('Parent', 'Guardian', 'Sibling'))
            emergency_contact_phone = fake.phone_number()
            medical_conditions = fake.sentence(nb_words=6)
            allergies = fake.sentence(nb_words=4)
            special_needs = fake.sentence(nb_words=5)
            notes = fake.sentence(nb_words=10)

            # Generate a fake image for the student
            img_byte_arr = io.BytesIO()
            image = Image.new('RGB', (720, 720), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            student = Student(
                name=name,
                dob=dob,
                gender=gender,
                nationality=nationality,
                current_status=current_status,
                cell=cell,
                village=village,
                sector=sector,
                district=district,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_relation=emergency_contact_relation,
                emergency_contact_phone=emergency_contact_phone,
                medical_conditions=medical_conditions,
                allergies=allergies,
                special_needs=special_needs,
                notes=notes,
                image=ContentFile(img_byte_arr, name=f'student_{slugify(name)}_{dob}_{gender}.jpeg')
            )
            student.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 30 fake students'))
