from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course
# Create your views here.


@login_required
def course_list_page(request):
    courses = Course.objects.all()
    return render(request, 'course/index.html', {'courses': courses})
