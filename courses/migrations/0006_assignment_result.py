# Generated by Django 5.0.2 on 2024-05-25 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_assignment_content_course_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='result',
            field=models.TextField(default='Result of assignment'),
        ),
    ]
