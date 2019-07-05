from django.urls import path

from . import views

urlpatterns = [
    path('handbook/', views.handbook, name='handbook_home'),
    path('handbook/<str:r_major>/<int:admission_year>/', views.handbook_content, name='handbook_content')
]
