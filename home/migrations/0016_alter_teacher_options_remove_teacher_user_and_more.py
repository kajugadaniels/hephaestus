# Generated by Django 5.0.4 on 2024-09-16 20:41

import home.models
import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_academicyear_created_by_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='user',
        ),
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=home.models.teacher_image_path),
        ),
        migrations.AddField(
            model_name='teacher',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
