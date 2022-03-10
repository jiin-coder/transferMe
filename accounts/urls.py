from django.urls import path, reverse_lazy
from . import views
from .forms import MyPasswordResetForm
from .views import MyPasswordResetView

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('find_username/', views.find_username, name='find_username'),
    path('edit/', views.edit, name='edit'),
]
