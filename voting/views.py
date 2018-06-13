from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from course.models import Course
from .models import QuickVotes


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
