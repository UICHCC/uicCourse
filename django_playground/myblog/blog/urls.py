from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path('article/<int:article_id>', views.article_page, name='post_page'),
]
