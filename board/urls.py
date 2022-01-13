from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('create/', views.Article_create, name='create'),
    path('list/', views.Article_list, name='list'),
]
