from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.messages import get_messages

import hashlib
import random

from . import models


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'course/index.html')
    else:
        userdata = request.user
        if get_messages(request):
            message = get_messages(request)
            messages.add_message(request, message.tags, message)
        return redirect('/course/')


def login_receiver(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/course/')
    else:
        messages.add_message(request, messages.ERROR, 'Wrong username or password.')
        return redirect('/')


def logout_receiver(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout successfully.')
    return redirect('/')


def course_list(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        userdata = request.user
        course_all = models.Course.objects.all()
        return render(request, 'course/course.html', {'userdata': userdata, 'courses': course_all})


def course_detail(request, course_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        userdata = request.user
        course_solo = models.Course.objects.get(pk=course_id)
        return render(request, 'course/detail.html', {'userdata': userdata, 'coursedata': course_solo})


def course_edit(request, course_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        userdata = request.user
        if str(course_id) == '0':
            return render(request, 'course/detail_edit.html', {'userdata': userdata})
        else:
            course_solo = models.Course.objects.get(pk=course_id)
            return render(request, 'course/detail_edit.html', {'userdata': userdata, 'coursedata': course_solo})


def course_edit_submit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        course_name_en = request.POST.get('cne')
        course_name_cn = request.POST.get('cnc')
        course_code = request.POST.get('cc')
        course_class = request.POST.get('cclass')
        course_units = request.POST.get('cu')
        course_descriptions = request.POST.get('cd')
        course_id = request.POST.get('cid')
        if course_id == '0':
            models.Course.objects.create(
                course_name_en=course_name_en,
                course_name_cn=course_name_cn,
                course_code=course_code,
                course_class=course_class,
                course_units=course_units,
                course_descriptions=course_descriptions,
            )
        else:
            modify_course = models.Course.objects.get(pk=course_id)
            modify_course.course_name_en = course_name_en
            modify_course.course_name_cn = course_name_cn
            modify_course.course_code = course_code
            modify_course.course_class = course_class
            modify_course.course_units = course_units
            modify_course.course_descriptions = course_descriptions
            modify_course.save()
        return redirect('/')


def delete_course(request, course_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        if course_id == '0':
            pass
        else:
            predelete = models.Course.objects.get(pk=course_id)
            predelete.delete()
        return redirect('/course/')


def signup_invite(request):
    if not request.user.is_authenticated:
        return render(request, 'course/signup.html')
    else:
        return redirect('/course/')


def signup_check(request):
    email = request.POST.get('email')
    un = request.POST.get('username')
    pw = request.POST.get('password')
    ic = request.POST.get('invitationcode')
    try:
        models.InvitationCode.objects.get(invitation_code=ic)
    except ObjectDoesNotExist:
        return redirect('/')

    user = User.objects.create_user(
        username=un,
        password=pw,
        email=email,
    )
    deleting_code = models.InvitationCode.objects.get(invitation_code=ic)
    deleting_code.delete()
    if user is not None:
        login(request, user)
        return redirect('/course/')


def invitation_code(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        userdata = request.user
        times = request.POST.get('amount')
        if times:
            for i in range(int(times)):
                generated_code = hashlib.md5(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
                models.InvitationCode.objects.create(
                    invitation_code=generated_code,
                    usability=True,
                )
        code_all = models.InvitationCode.objects.all()
        return render(request, 'course/newic.html', {'userdata': userdata, 'codes': code_all})


def invitation_code_invalid(request, code_id):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        userdata = request.user
        deleting_code = models.InvitationCode.objects.get(pk=code_id)
        deleting_code.delete()
        code_all = models.InvitationCode.objects.all()
        return render(request, 'course/newic.html', {'userdata': userdata, 'codes': code_all})


def account_info_view(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        userdata = request.user
        return render(request, 'account/info.html', {'userdata': userdata})


def account_info_edit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        userdata = request.user
        return render(request, 'account/edit.html', {'userdata': userdata})


def account_info_submit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        first_name = request.POST.get('fn')
        last_name = request.POST.get('ln')
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('/account')


def account_password_edit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        userdata = request.user
        return render(request, 'account/password.html', {'userdata': userdata})


def account_password_submit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        old_password = request.POST.get('opw')
        if request.user.check_password(old_password):
            user = User.objects.get(id=request.user.id)
            user.set_password(request.POST.get('pw'))
            user.save()
            # user.save() is required after change password
            logout(request)
            return redirect('/')
        else:
            return redirect('/account/password/')
