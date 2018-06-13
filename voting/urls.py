from django.urls import path

from . import views

urlpatterns = [
    path('voting/quick_vote/<int:course_id>', views.vote_course, name='vote_course'),
]
