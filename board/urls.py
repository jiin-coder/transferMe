from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('create/', views.Article_write, name='write'),
    path('list/', views.Article_list, name='list'),
    path('detail/<int:article_id>/', views.Article_detail, name='detail'),
    path('article/modify/<int:article_id>/', views.article_modify, name='article_modify'),
    path('article/delete/<int:article_id>/', views.article_delete, name='article_delete'),
]
