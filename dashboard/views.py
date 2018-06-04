from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# from django.contrib.messages import get_messages
from django.http import JsonResponse

# Create your views here.


def welcome_page(request):
    return render(request, 'index/index.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Login successfully.')
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Wrong username or password.')
            return redirect('/')
    else:
        return render(request, 'index/login.html')


def logout_receiver(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout successfully.')
    return redirect('/')


def signup_page(request):
    return render(request, 'index/signup.html')
