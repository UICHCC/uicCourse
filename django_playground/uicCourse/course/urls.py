from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('?error=<int:error_number>', views.index_error),
    path('login/', views.login_receiver, name='login_receiver'),
    path('logout/', views.logout_receiver, name='logout_receiver'),
    path('course/', views.course_list, name='course_list'),
    path('course/<int:course_id>', views.course_detail, name='course_detail'),
    path('course/edit/<int:course_id>', views.course_edit, name='course_detail_edit'),
    path('course/edit_submit', views.course_edit_submit),
]
