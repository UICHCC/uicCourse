from django.urls import path

from . import views

urlpatterns = [
    path('course/', views.course_list_page, name='course_list_page'),
]
