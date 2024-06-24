from django import forms
from .models import Course, Assignment, TestCase

from django.forms import Textarea, TextInput

class CourseForm(forms.ModelForm):
    name = forms.CharField(label='Название курса', widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Название курса'}))
    topic = forms.ChoiceField(label='Тема курса', widget=forms.Select(attrs={'class': 'form-control'}), choices=Course.TOPIC_CHOICES)
    description = forms.CharField(label='Описание курса', widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание курса'}))
    content = forms.CharField(label='Содержание курса', widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Содержание курса'}))
    class Meta:
        model = Course
        fields = ['name', 'topic', 'description', 'content']

class AssignmentForm(forms.ModelForm):
    title = forms.CharField(label='Название задания', widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Название задания'}))
    description = forms.CharField(label='Описание задания', widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание задания'}))
    content = forms.CharField(label='Содержание задания', widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Содержание задания'}))

    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'content']

class TestCaseForm(forms.ModelForm):
    input_values = forms.CharField(label='Входные данные', widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Входные данные'}))
    expected_output = forms.CharField(label='Ожидаемый вывод', widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Ожидаемый вывод'}))

    class Meta:
        model = TestCase
        fields = ['input_values', 'expected_output']
