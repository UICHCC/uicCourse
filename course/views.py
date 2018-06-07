from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# from django.contrib.messages import get_messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def course_list_page(request):
    return render(request, 'course/index.html')