from django.urls import path

from . import views

urlpatterns = [
    path('course/', views.course_list_page, name='course_list_page'),
    path('neo/', views.course_list_neo, name='course_list_neo'),
    path('course/new/', views.course_create, name='course_create'),
    path('course/modify/<int:course_id>', views.course_modify, name='course_modify'),
    path('course/detail/<int:course_id>', views.course_detail, name='course_detail'),
    path('course/delete/<int:course_id>', views.course_delete, name='course_delete'),
]
