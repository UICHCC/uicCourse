from django.urls import path

from . import views

urlpatterns = [
    path('report/', views.report, name='report'),
    path('report/graph-api/', views.dependency_graph_api, name='graph-api')
]
