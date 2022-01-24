from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

from .models import Article, Comment


class ArticleWriteForm(forms.ModelForm):
    # pass1
    class Meta:
        model = Article  # 사용할 모델
        # Form에서 사용할 모델의 속성
        fields = [
            'title',
            'body',
            'one_source',
            'information_source'
        ]

        widgets = {
            'body': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'one_source': forms.TextInput(attrs={'class': 'form-control'}),
            'information_source': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': '제목',
            'body': '내용',
            'one_source': '출처',
            'information_source': '출처링크',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
