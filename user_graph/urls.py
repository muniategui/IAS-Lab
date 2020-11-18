from django.urls import path
from user_graph import views

urlpatterns = [
    path('graph', views.user_graph, name='user_graph'),
]
