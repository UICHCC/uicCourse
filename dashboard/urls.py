from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_receiver, name='logout_receiver'),
    path('signup/', views.signup_page, name='signup_page'),
    path('dashboard/change_password/', views.change_password_page, name='change_password'),
    path('about/terms', views.terms_page, name='terms_page'),
    path('about/privacy', views.privacy_page, name='privacy_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/course/major_division', views.major_division, name='major_division'),
    path('dashboard/course/course_type', views.course_type, name='course_type'),
    path('dashboard/tags/', views.tags_page, name='tags_page'),
    path('dashboard/tags/create', views.tags_create, name='tags_create'),
    path('dashboard/tags/modify/<int:tag_id>', views.tags_modify, name='tags_modify'),
    path('dashboard/tags/delete/<int:tag_id>', views.tags_delete, name='tags_delete'),
]
