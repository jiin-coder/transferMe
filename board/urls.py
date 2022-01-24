from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('create/', views.Article_write, name='write'),
    path('list/', views.Article_list, name='list'),
    path('detail/<int:article_id>/', views.Article_detail, name='detail'),
    path('article/modify/<int:article_id>/', views.article_modify, name='article_modify'),
    path('article/delete/<int:article_id>/', views.article_delete, name='article_delete'),
    path('vote/article/<int:article_id>/', views.vote_article, name='vote_article'),
    path('comment/create/article/<int:article_id>/', views.comment_create_article, name='comment_create_article'),
    path('comment/modify/article/<int:comment_id>/', views.comment_modify_article, name='comment_modify_article'),
    path('comment/delete/article/<int:comment_id>/', views.comment_delete_article, name='comment_delete_article'),
]
