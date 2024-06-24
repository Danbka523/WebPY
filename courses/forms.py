from django import forms
from .models import Course, Assignment, TestCase

from django.forms import Textarea, TextInput

class CourseForm(forms.ModelForm):
    name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Course name'}))
    topic = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Course.TOPIC_CHOICES)
    description = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Course description'}))
    content = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Course content'}))
    class Meta:
        model = Course
        fields = ['name', 'topic', 'description', 'content']

class AssignmentForm(forms.ModelForm):
    title = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Assignment title'}))
    description = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Assignment description'}))
    content = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Assignment content'}))

    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'content']

class TestCaseForm(forms.ModelForm):
    input_values = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Input values'}))
    expected_output = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Expected output'}))

    class Meta:
        model = TestCase
        fields = ['input_values', 'expected_output']
