from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect


from course.models import Course
from .models import QuickVotes, Tags, UserTaggingCourse


@login_required
def vote_course(request, course_id):
    action = request.GET.get('vote_action')
    current_course = Course.objects.get(pk=course_id)
    try:
        user_quickvote = QuickVotes.objects.get(course=current_course, voter=request.user.id)
    except ObjectDoesNotExist:
        if action == 'upvote':
            QuickVotes.objects.create(
                course=current_course,
                voter=request.user,
                vote_status=1,
            )
        elif action == 'downvote':
            QuickVotes.objects.create(
                course=current_course,
                voter=request.user,
                vote_status=0,
            )
        data = {
            'is_success': True,
            'new_upvote': QuickVotes.objects.filter(course=course_id, vote_status=True, is_invalid_vote=0).count(),
        }
        return JsonResponse(data)
    if action == 'upvote':
        user_quickvote.vote_status = 1
    elif action == 'downvote':
        user_quickvote.vote_status = 0
    user_quickvote.save()
    valid_upvote = QuickVotes.objects.filter(course=course_id, vote_status=True, is_invalid_vote=0).count()
    valid_downvote = QuickVotes.objects.filter(course=course_id, vote_status=False, is_invalid_vote=0).count()
    if valid_upvote + valid_downvote == 0:
        course_score = 5
    elif valid_downvote == 0:
        course_score = 10
    elif valid_upvote == 0:
        course_score = 2
    else:
        course_score = 2 + 8 * (valid_upvote / (valid_upvote + valid_downvote))
    data = {
        'is_success': True,
        'new_upvote': int(QuickVotes.objects.filter(course=course_id, vote_status=True, is_invalid_vote=0).count()),
        'current_score': course_score,
    }
    return JsonResponse(data)


@login_required
def tag_course(request):
    tagging_course = Course.objects.get(pk=request.POST.get('course_id'))
    try:
        UserTaggingCourse.objects.get(tag_course=tagging_course, tagger=request.user)
        messages.warning(request, 'You have already submit your review to this course!')
        return redirect('/course/detail/' + request.POST.get('course_id'))
    except ObjectDoesNotExist:
        new_review = UserTaggingCourse.objects.create(tag_course=tagging_course, tagger=request.user)
        new_review.save()
        if request.POST.get('tag1') != '':
            new_review.tags.add(Tags.objects.get(pk=request.POST.get('tag1')))
        if request.POST.get('tag2') != '':
            new_review.tags.add(Tags.objects.get(pk=request.POST.get('tag2')))
        if request.POST.get('tag3') != '':
            new_review.tags.add(Tags.objects.get(pk=request.POST.get('tag3')))
        messages.success(request, 'Your review have been successfully create!')
        return redirect('/course/detail/' + request.POST.get('course_id'))
