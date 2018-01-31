from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from . import models


def index(request):
    return render(request, 'course/index.html')


def login_receiver(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/course/')
    else:
        return HttpResponse('No way')


def logout_receiver(request):
    logout(request)
    return redirect('/')


def course_list(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return HttpResponse('Login user can see this course_list')


def course_detail(request):
    return HttpResponse('This is a course detail page')


def course_edit(request):
    return HttpResponse('This is a course edit page')


def course_edit_submit(request):
    return HttpResponse('submit received')
