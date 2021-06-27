from django.shortcuts import render
from django.db.models import Q

from course.models import Course
# Create your views here.


def search_course(request):
    raw_input = request.GET.get('search')
    search_result = ''
    if raw_input is not None:
        search_result = Course.objects.filter(Q(course_id__icontains=raw_input) | Q(course_name_en__icontains=raw_input) | Q(course_name_cn__icontains=raw_input))
    return render(request, 'index/search.html', {'search_result': search_result, 'raw_input': raw_input})


# def search_matching(request):
#     if request.method == 'POST':
