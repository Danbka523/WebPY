from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    TOPIC_CHOICES = [
        ('python', 'Основы Python'),
        ('web', 'Основы Web на Python'),
        ('django', 'Основы Django'),
    ]

    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES)
    description = models.TextField(default="Short description")
    content = models.TextField(default="Text of the course")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name
    
class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(default="Short description")
    content = models.TextField(default="Text of assignment")
    created_at = models.DateTimeField(auto_now_add=True)
    test_cases_count = models.IntegerField(default=5)
    
    def __str__(self):
        return self.title
    
class TestCase(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='test_cases', on_delete=models.CASCADE)
    input_values = models.TextField(help_text="Input values as a comma-separated string")
    expected_output = models.CharField(max_length=200)

    def __str__(self):
        return f"Test Case for {self.assignment.title}"