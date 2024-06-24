from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.forms import inlineformset_factory
from .models import Course, Assignment, TestCase
from .forms import CourseForm, AssignmentForm, TestCaseForm


def course_list(request):
    topic = request.GET.get('topic', '')
    if topic:
        courses = Course.objects.filter(topic=topic)
    else:
        courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course_detail.html', {'course': course})

@login_required
def create_course(request):
    if not check_group(request.user):
        return redirect('course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

@login_required
def edit_course(request,course_id):
    if not check_group(request.user):
        return redirect('course_list')
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'course': course})

@login_required
def add_assignment(request, course_id, test_cases_count=5):  
    if not check_group(request.user):
        return redirect('course_list')
    TestCaseFormSet = inlineformset_factory(Assignment, TestCase, form=TestCaseForm, extra=test_cases_count)
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        formset = TestCaseFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            test_cases = formset.save(commчit=False)
            for test_case in test_cases:
                test_case.assignment = assignment
                test_case.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = AssignmentForm()
        formset = TestCaseFormSet
    return render(request, 'create_assignment.html', {'form': form, 'course': course, 'formset': formset})

@login_required
def assignment_detail(request, course_id, assignment_id):
    if not check_group(request.user):
        return redirect('course_list')
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id, course=course)
    return render(request, 'assignment_detail.html', {'course': course, 'assignment': assignment})

def edit_assignment(request,course_id,assignment_id):
    if not check_group(request.user):
        return redirect('course_list')
    assignment = get_object_or_404(Assignment, id=assignment_id)
    TestCaseFormSet = inlineformset_factory(Assignment, TestCase, form=TestCaseForm, extra=assignment.test_cases_count)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        formset = TestCaseFormSet(request.POST, instance=assignment)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = AssignmentForm(instance=assignment)
        formset = TestCaseFormSet(instance=assignment)
    return render(request, 'edit_assignment.html', {'form': form, 'formset': formset})



def check_group(user):
    return user.groups.filter(name='Teachers').exists() or user.is_superuser