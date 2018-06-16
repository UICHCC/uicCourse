from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
from .forms import CourseForm
from voting.models import QuickVotes, Tags, UserTaggingCourse
# Create your views here.


@login_required
def course_list_page(request):
    courses_list = Course.objects.all().order_by('id')
    paginator = Paginator(courses_list, 15)
    page = request.GET.get('page')
    courses = paginator.get_page(page)
    return render(request, 'course/index.html', {'courses': courses})


@staff_member_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'The Course: ' + course.course_name_en + ' was successfully created!')
            return redirect('/course/?page=9999')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CourseForm()
    return render(request, 'course/course_create.html', {'form': form})


@staff_member_required
def course_modify(request, course_id):
    if request.method == 'POST':
        changing_course = Course.objects.get(pk=course_id)
        form = CourseForm(data=request.POST, instance=changing_course)
        if form.is_valid():
            form.save()
            messages.success(request, 'The Course was been successfully modified!')
            return redirect('/course/' + str(course_id))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        course = Course.objects.get(pk=course_id)
        form = CourseForm(instance=course)
    return render(request, 'course/course_create.html', {'form': form})


@staff_member_required
def course_delete(request, course_id):
    course = Course.objects.get(pk=course_id)
    course.delete()
    messages.success(request, 'The Course was been successfully deleted!')
    return redirect('/course/')


@login_required
def course_detail(request, course_id):
    query_course = Course.objects.get(pk=course_id)
    majors_take = query_course.course_major_take.all()
    division_involve = []
    for item in majors_take:
        if item.division.division_en_abbr not in division_involve:
            division_involve.append(item.division.division_en_abbr)
    is_voted = True
    try:
        user_vote = QuickVotes.objects.get(course=query_course, voter=request.user)
    except ObjectDoesNotExist:
        user_vote = QuickVotes.objects.filter(course=query_course, voter=request.user)
        is_voted = False
    valid_upvote = QuickVotes.objects.filter(course=query_course, vote_status=True, is_invalid_vote=0).count()
    valid_downvote = QuickVotes.objects.filter(course=query_course, vote_status=False, is_invalid_vote=0).count()
    if valid_upvote + valid_downvote == 0:
        course_score = 5
    elif valid_downvote == 0:
        course_score = 10
    elif valid_upvote == 0:
        course_score = 2
    else:
        course_score = 2 + 8 * (valid_upvote / (valid_upvote + valid_downvote))
    vote_status = {
        'upvote': valid_upvote,  # True = up vote, False = down vote
        'downvote': valid_downvote,
        'score': course_score,
    }
    available_tags = Tags.objects.all()
    course_tag_data = {}
    for item in query_course.course_tags.all():
        for tag in item.tags.all():
            if tag.tag_title in course_tag_data:
                course_tag_data[tag.tag_title] += 1
            else:
                course_tag_data[tag.tag_title] = 1
    print(course_tag_data)
    try:
        user_review = UserTaggingCourse.objects.get(tag_course=query_course, tagger=request.user)
    except ObjectDoesNotExist:
        user_review = UserTaggingCourse.objects.filter(tag_course=query_course, tagger=request.user)
    return render(request, 'course/course_detail.html', {'course_data': query_course,
                                                         'majors': majors_take,
                                                         'division_involve': division_involve,
                                                         'is_voted': is_voted,
                                                         'user_vote': user_vote,
                                                         'course_vote_status': vote_status,
                                                         'available_tags': available_tags,
                                                         'course_tag_data': course_tag_data,
                                                         'user_review': user_review})
