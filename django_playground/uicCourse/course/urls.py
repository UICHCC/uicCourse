from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login, name='login_receiver'),
    path('course/', views.course_list),
    path('course/<int:course_code>', views.course_detail),
    path('course/edit/<int:course_code>', views.course_edit),
    path('course/edit_submit', views.course_edit_submit),
]
