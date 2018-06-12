from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course
from .forms import CourseForm
# Create your views here.


@login_required
def course_list_page(request):
    courses = Course.objects.all()
    return render(request, 'course/index.html', {'courses': courses})


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'The Course: ' + course.course_name_en + ' was successfully created!')
            return redirect('/course/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CourseForm()
    return render(request, 'course/course_create.html', {'form': form})


@login_required
def course_modify(request, course_id):
    if request.method == 'POST':
        changing_course = Course.objects.get(pk=course_id)
        form = CourseForm(data=request.POST, instance=changing_course)
        if form.is_valid():
            form.save()
            messages.success(request, 'The Course was been successfully modified!')
            return redirect('/course/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        course = Course.objects.get(pk=course_id)
        form = CourseForm(instance=course)
    return render(request, 'course/course_create.html', {'form': form})
