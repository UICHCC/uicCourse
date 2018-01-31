from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from . import models


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'course/index.html')
    else:
        userdata = request.user
        return redirect('/course/')


def index_error(request, error_number):
    if str(error_number) == '1':
        return render(request, 'course/index.html', {'errormessage': 'Wrong Username or password.'})
    elif str(error_number) == '2':
        return render(request, 'course/index.html', {'errormessage': 'Logout successfully.'})
    else:
        return render(request, 'course/index.html', {'errormessage': "Don't Play that error number!"})


def login_receiver(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/course/')
    else:
        return redirect('/')


def logout_receiver(request):
    logout(request)
    return redirect('/')


def course_list(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        userdata = request.user
        course_all = models.Course.objects.all()
        return render(request, 'course/course.html', {'userdata': userdata, 'courses': course_all})


def course_detail(request, course_id):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        userdata = request.user
        course_solo = models.Course.objects.get(pk=course_id)
        return render(request, 'course/detail.html', {'userdata': userdata, 'coursedata': course_solo})


def course_edit(request, course_id):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        userdata = request.user
        course_solo = models.Course.objects.get(pk=course_id)
        return render(request, 'course/detail_edit.html', {'userdata': userdata, 'coursedata': course_solo})


def course_edit_submit(request):
    return HttpResponse('submit received')
