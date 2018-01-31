from django.shortcuts import render

from django.contrib.auth import authenticate


def index(request):
    return render(request, 'course/index.html')


def login(request):
    return 'Login!'

def course_list(request):
    return 'This is a course list'


def course_detail(request):
    return 'This is a course detail page'


def course_edit(request):
    return 'This is a course edit page'


def course_edit_submit(request):
    return 'submit received'
