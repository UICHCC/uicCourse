from django.urls import path

from . import views

urlpatterns = [
    path('course/', views.course_list_page, name='course_list_page'),
    path('course/new/', views.course_create, name='course_create'),
    path('course/modify/<int:course_id>', views.course_modify, name='course_modify'),
]
