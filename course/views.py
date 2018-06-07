from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def course_list_page(request):
    return render(request, 'course/index.html')