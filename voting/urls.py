from django.urls import path

from . import views

urlpatterns = [
    path('voting/quick_vote/<int:course_id>', views.vote_course, name='vote_course'),
    path('voting/tag_course/', views.tag_course, name='tag_course')
]
