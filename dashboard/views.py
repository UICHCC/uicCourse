from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# from django.contrib.messages import get_messages
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import SignUpForm

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
            return redirect('/course/')
        else:
            messages.add_message(request, messages.ERROR, 'Wrong username or password.')
            return redirect('/login/')
    else:
        if not request.user.is_authenticated:
            return render(request, 'index/login.html')
        else:
            messages.add_message(request, messages.ERROR, 'No Double Login Is Allowed.')
            return redirect('/')


def logout_receiver(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout successfully.')
    return redirect('/')


def signup_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Sign up successfully.')
                return redirect('/course/')
        else:
            form = SignUpForm()
        return render(request, 'index/signup.html', {'form': form})
    else:
        messages.add_message(request, messages.ERROR, 'Not Allow.')
        return redirect('/')


def change_password_page(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/course/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'index/change_password.html', {'form': form})


def terms_page(request):
    return render(request, 'index/terms.html')


def privacy_page(request):
    return render(request, 'index/privacy.html')
