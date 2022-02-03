import os

import requests
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (
    logout_then_login, LoginView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from lazy_string import LazyString

from .decorators import logout_required
from .forms import SignupForm, FindUsernameForm
from .models import User

@logout_required
def signin(request: HttpRequest):
    return LoginView.as_view(template_name="accounts/signin.html")(request)


def signout(request: HttpRequest):
    messages.success(request, "로그아웃 되었습니다.")
    return logout_then_login(request)


@logout_required
def signup(request: HttpRequest):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입 환영합니다.")
            # signed_user.send_welcome_email()
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })





class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = "accounts/signin.html"
    next_page = "/"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.success_message = LazyString(
            lambda: f'{self.request.user.last_name}{self.request.user.first_name}님 환영합니다.')

    def get_initial(self):
        initial = self.initial.copy()
        initial['username'] = self.request.GET.get('username', None)

        return initial



def find_username(request: HttpRequest):
    if request.method == 'POST':
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']

            qs: QuerySet = User.objects.filter(email=email, first_name=first_name)

            if not qs.exists():
                messages.warning(request, "일치하는 회원이 존재하지 않습니다.")
            else:
                user: User = qs.first()
                messages.success(request, f"해당회원의 username은 {user.username} 입니다.")
                return redirect(reverse("accounts:signin") + '?username=' + user.username)
    else:
        form = FindUsernameForm()

    return render(request, 'accounts/find_username.html', {
        'form': form,
    })


def kakao_login(request: HttpRequest):
    REST_API_KEY = os.environ.get("KAKAO_APP__REST_API_KEY")
    REDIRECT_URI = os.environ.get("KAKAO_APP__LOGIN__REDIRECT_URI")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


def kakao_login_callback(request):
    code = request.GET.get("code")

    REST_API_KEY = os.environ.get("KAKAO_APP__REST_API_KEY")
    REDIRECT_URI = os.environ.get("KAKAO_APP__LOGIN__REDIRECT_URI")

    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
    )

    token_json = token_request.json()

    error = token_json.get("error", None)
    if error is not None:
        raise Exception("카카오 로그인 에러")

    access_token = token_json.get("access_token")

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()

    id = profile_json.get("id")

    User.login_with_kakao(request, id)

    messages.success(request, "카카오톡 계정으로 로그인되었습니다")

    return redirect("index")