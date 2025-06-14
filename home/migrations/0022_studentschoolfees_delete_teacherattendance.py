# Generated by Django 5.0.4 on 2024-09-17 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_alter_teacherattendance_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentSchoolFees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('due_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.academicyear')),
                ('class_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.term')),
            ],
        ),
        migrations.DeleteModel(
            name='TeacherAttendance',
        ),
    ]
