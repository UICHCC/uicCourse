from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required


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
    tag_data = []
    tag_data.append(Course.objects.get(pk=request.POST.get('course_id')).course_name_en)
    if request.POST.get('tag1') != '':
        tag_data.append(Tags.objects.get(pk=request.POST.get('tag1')).tag_title)
    if request.POST.get('tag2') != '':
        tag_data.append(Tags.objects.get(pk=request.POST.get('tag2')).tag_title)
    if request.POST.get('tag3') != '':
        tag_data.append(Tags.objects.get(pk=request.POST.get('tag3')).tag_title)
    return HttpResponse(tag_data)
