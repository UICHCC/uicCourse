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