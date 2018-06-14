from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import SignUpForm, CreateTagForm

from course.models import ValidDivisionMajorPair, CourseType
from voting.models import Tags


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
            messages.add_message(request, messages.INFO, 'Login is require to continue.')
            return render(request, 'auth/login.html')
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
        return render(request, 'auth/signup.html', {'form': form})
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
    return render(request, 'auth/change_password.html', {'form': form})


def terms_page(request):
    return render(request, 'index/terms.html')


def privacy_page(request):
    return render(request, 'index/privacy.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard/index.html')


@staff_member_required
def major_division(request):
    pairs = ValidDivisionMajorPair.objects.all()
    return render(request, 'dashboard/major_division.html', {'pairs': pairs})


@staff_member_required
def course_type(request):
    pairs = CourseType.objects.all()
    return render(request, 'dashboard/course_type.html', {'pairs': pairs})


@staff_member_required
def tags_page(request):
    tags = Tags.objects.all()
    return render(request, 'dashboard/tags.html', {'tags': tags})


@staff_member_required
def tags_create(request):
    if request.method == 'POST':
        form = CreateTagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, 'The Tag: ' + tag.tag_title + ' was successfully created!')
            return redirect('/dashboard/tags/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CreateTagForm()
    return render(request, 'dashboard/tag_create.html', {'form': form})


@staff_member_required
def tags_modify(request, tag_id):
    if request.method == 'POST':
        changing_tag = Tags.objects.get(pk=tag_id)
        form = CreateTagForm(data=request.POST, instance=changing_tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'The tag has been successfully modified!')
            return redirect('/dashboard/tags/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        tag = Tags.objects.get(pk=tag_id)
        form = CreateTagForm(instance=tag)
        return render(request, 'dashboard/tag_create.html', {'form': form, 'is_modify': True, 'tag_id': tag.id})


@staff_member_required
def tags_delete(request, tag_id):
    delete_tag = Tags.objects.get(pk=tag_id)
    delete_tag.delete()
    messages.success(request, 'The tag has been successfully deleted!')
    return redirect('/dashboard/tags/')
