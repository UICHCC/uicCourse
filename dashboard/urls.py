from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_receiver, name='logout_receiver'),
    path('signup/', views.signup_page, name='signup_page'),
]