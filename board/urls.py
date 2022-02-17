from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('create/', views.article_write, name='write'),
    path('list/', views.article_list, name='list'),
    path('myposts/', views.my_article, name='myposts'),
    path('article/detail/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/modify/<int:article_id>/', views.article_modify, name='article_modify'),
    path('article/delete/<int:article_id>/', views.article_delete, name='article_delete'),
    path('article/vote/<int:article_id>/', views.vote_article, name='vote_article'),
    path('article/<int:article_id>/comment/', views.comment_create, name='comment_create'),
    path('article/<int:article_id>/comment/delete/<int:comment_id>', views.comment_delete, name='comment_delete'),
    path('article/<int:article_id>/comment/modify/<int:comment_id>', views.comment_modify, name='comment_modify'),
]
