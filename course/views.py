from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# from django.contrib.messages import get_messages

import hashlib
import random

from . import models


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'course/index.html')
    else:
        return redirect('/course/')


def login_receiver(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Login successfully.')
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
        course_all = models.Course.objects.all()
        return render(request, 'course/course.html', {'courses': course_all})


def course_detail(request, course_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        course_solo = models.Course.objects.get(pk=course_id)
        course_comment = models.Comments.objects.filter(course=course_id)
        is_commented = True
        try:
            user_comment = models.Comments.objects.get(course=course_solo, sender=request.user)
        except ObjectDoesNotExist:
            user_comment = models.Comments.objects.filter(course=course_solo, sender=request.user)
            is_commented = False
        return render(request, 'course/detail.html', {'coursedata': course_solo,
                                                      'coursecomments': course_comment,
                                                      'is_commented': is_commented,
                                                      'user_comment': user_comment,
                                                      })


def course_edit(request, course_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        if str(course_id) == '0':
            return render(request, 'course/detail_edit.html')
        else:
            course_solo = models.Course.objects.get(pk=course_id)
            return render(request, 'course/detail_edit.html', {'coursedata': course_solo})


def course_edit_submit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        course_name_en = request.POST.get('cne')
        course_name_cn = request.POST.get('cnc')
        course_code = request.POST.get('cc')
        course_class = request.POST.get('cclass')
        course_units = request.POST.get('cu')
        course_descriptions = request.POST.get('cd')
        course_id = request.POST.get('cid')
        if str(course_id) == '0':
            models.Course.objects.create(
                course_name_en=course_name_en,
                course_name_cn=course_name_cn,
                course_code=course_code,
                course_class=course_class,
                course_units=course_units,
                course_descriptions=course_descriptions,
            )
            messages.add_message(request, messages.SUCCESS, 'Created course information successfully.')
        else:
            modify_course = models.Course.objects.get(pk=course_id)
            modify_course.course_name_en = course_name_en
            modify_course.course_name_cn = course_name_cn
            modify_course.course_code = course_code
            modify_course.course_class = course_class
            modify_course.course_units = course_units
            modify_course.course_descriptions = course_descriptions
            modify_course.save()
            messages.add_message(request, messages.SUCCESS, 'Modify the course information successfully.')
        return redirect('/')


def course_comments_submit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        comment_id = request.POST.get('comment_id')
        comments = request.POST.get('comments')
        course_code = request.POST.get('course_id')
        if comment_id is not '':
            comment_object = models.Comments.objects.get(id=comment_id)
            comment_object.content = comments
            comment_object.save()
            messages.add_message(request, messages.SUCCESS, 'Comments edited.')
        else:
            course_object = models.Course.objects.get(pk=course_code)
            user_object = request.user
            models.Comments.objects.create(course=course_object,
                                           sender=user_object,
                                           content=comments)
            messages.add_message(request, messages.SUCCESS, 'Comments submitted.')
        return redirect('/course/' + course_code + '/')


def delete_course(request, course_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        if course_id == '0':
            pass
        else:
            predelete = models.Course.objects.get(pk=course_id)
            predelete_name = predelete.course_name_en
            predelete.delete()
            messages.add_message(request, messages.SUCCESS, 'Delete the course: ' + predelete_name + ' successfully.')
        return redirect('/course/')


def signup_invite(request):
    if not request.user.is_authenticated:
        return render(request, 'course/signup.html')
    else:
        messages.add_message(request, messages.WARNING, 'You are logged in.')
        return redirect('/course/')


def signup_check(request):
    if request.user.is_authenticated:
        return redirect('/course/')
    else:
        email = request.POST.get('email')
        un = request.POST.get('username')
        pw = request.POST.get('password')
        ic = request.POST.get('invitationcode')
        try:
            models.InvitationCode.objects.get(invitation_code=ic)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Invalid invitation code.')
            return redirect('/signup/')

        user = User.objects.create_user(
            username=un,
            password=pw,
            email=email,
        )
        deleting_code = models.InvitationCode.objects.get(invitation_code=ic)
        deleting_code.delete()
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Signup Successfully.')
            return redirect('/course/')


def admin_tools(request):
    return render(request, 'tools/index.html')


def invitation_code(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        times = request.POST.get('amount')
        if times:
            for i in range(int(times)):
                generated_code = hashlib.md5(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
                models.InvitationCode.objects.create(
                    invitation_code=generated_code,
                    usability=True,
                )
        code_all = models.InvitationCode.objects.all()
        if times is not None:
            messages.add_message(request, messages.INFO, 'Generated ' + str(times) + ' new invitation code(s).')
    return render(request, 'tools/newic.html', {'codes': code_all})


def invitation_code_invalid(request, code_id):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        deleting_code = models.InvitationCode.objects.get(pk=code_id)
        deleted_code = deleting_code.invitation_code
        deleting_code.delete()
        code_all = models.InvitationCode.objects.all()
        messages.add_message(request, messages.SUCCESS, 'Code: ' + deleted_code + ' invalided.')
        return render(request, 'tools/newic.html', {'codes': code_all})


def account_info_view(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Login required.')
        return redirect('/')
    else:
        return render(request, 'account/info.html')


def account_info_edit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        return render(request, 'account/edit.html')


def account_info_submit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        first_name = request.POST.get('fn')
        last_name = request.POST.get('ln')
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Modify successfully.')
        return redirect('/account')


def account_password_edit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        return render(request, 'account/password.html')


def account_password_submit(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        old_password = request.POST.get('opw')
        if request.user.check_password(old_password):
            user = User.objects.get(id=request.user.id)
            user.set_password(request.POST.get('pw'))
            user.save()
            # user.save() is required after change password
            logout(request)
            messages.add_message(request, messages.SUCCESS, 'Change password successfully.')
            messages.add_message(request, messages.INFO, 'Need to re-login')
            return redirect('/')
        else:
            messages.add_message(request, messages.WARNING, 'Old password does not match.')
            return redirect('/account/password/')


def user_info_view(request,user_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        if str(user_id) == str(request.user.id):
            return redirect('/account/')
        else:
            request_userdata = models.User.objects.get(pk=user_id)
            return render(request, 'account/see.html', {'aim_user': request_userdata})


def comment_operation(request, comment_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'No permission.')
        return redirect('/')
    else:
        comment_object = models.Comments.objects.get(pk=comment_id)
        operation = request.POST.get('operation')
        if operation == 'ban':
            comment_object.is_banned = True
            messages.add_message(request, messages.INFO, str('Comment' + str(comment_id) + ' Banned Successfully.'))
        elif operation == 'undoban':
            comment_object.is_banned = False
            messages.add_message(request, messages.INFO, str('Comment' + str(comment_id) + ' Undo Ban Successfully.'))
        elif operation == 'recommend':
            comment_object.is_recommend = True
            messages.add_message(request, messages.INFO, str('Comment' + str(comment_id) + ' Recommend Successfully.'))
        elif operation == 'undorecommend':
            comment_object.is_recommend = False
            messages.add_message(request, messages.INFO, str('Comment' + str(comment_id) + ' Undo Recommend Successfully.'))
        comment_object.save()
    return redirect('/course/' + str(comment_object.course.id) + '/')


def handler404(request):
    return render(request, 'error/404.html', status=404)


def handler500(request):
    return render(request, 'error/500.html', status=500)

