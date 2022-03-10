
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    logout_then_login, LoginView, PasswordResetView, PasswordResetConfirmView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, redirect

from django.urls import reverse
from lazy_string import LazyString

from .decorators import logout_required
from .forms import SignupForm, FindUsernameForm, UserEditForm
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
            lambda: f'{self.request.user.last_name}{self.request.user.username}님 환영합니다.')

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
                messages.success(request, f"해당회원의 닉네임은 {user.username} 입니다.")
                return redirect(reverse("accounts:signin") + '?username=' + user.username)
    else:
        form = FindUsernameForm()

    return render(request, 'accounts/find_username.html', {
        'form': form,
    })

@login_required
def edit(request: HttpRequest):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "회원정보가 수정되었습니다.")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'accounts/edit.html', {
        'form': form,
    })

class MyPasswordResetView(SuccessMessageMixin, PasswordResetView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.success_message = "비밀번호가 재설정 되었습니다."

