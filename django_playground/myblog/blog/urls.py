from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path('article/<int:article_id>', views.article_page, name='post_page'),
    path('edit/<int:article_id>', views.edit_page, name='edit_page'),
    path('edit/action/', views.edit_page_db, name='edit_new'),
]
