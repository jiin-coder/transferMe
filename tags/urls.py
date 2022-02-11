from django.urls import path

from tags import views

app_name = "tags"

urlpatterns = [
    path('hashtag/', views.hashtag, name="hashtag"),
]
