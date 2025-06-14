# Generated by Django 5.0.4 on 2024-09-03 09:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_classsubject_created_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='academic_years_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='academic_years_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
