from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm

from accounts.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = '닉네임'


# username : 닉네임
# email : 이메일 주소로 로그인
# first_name : 실제 이름
class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].label = '닉네임'
        self.fields['first_name'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email


class UserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['username'].label = '닉네임'
        self.fields['password'].widget = forms.HiddenInput()

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['first_name', 'username', 'email', 'password']

    def clean_email(self):
        first_name = self.cleaned_data.get('first_name')
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email).exclude(first_name=first_name)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email


class FindUsernameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True

    class Meta:
        model = User
        fields = ['first_name', 'email']


