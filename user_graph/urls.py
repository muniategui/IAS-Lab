from django.urls import path
from user_graph import views

urlpatterns = [
    path('graph', views.hello_world, name='hello_world'),
]
