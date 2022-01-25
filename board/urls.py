from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('create/', views.article_write, name='write'),
    path('list/', views.article_list, name='list'),
    path('article/detail/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/modify/<int:article_id>/', views.article_modify, name='article_modify'),
    path('article/delete/<int:article_id>/', views.article_delete, name='article_delete'),
    path('article/vote/<int:article_id>/', views.vote_article, name='vote_article')
]
