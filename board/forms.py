from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # 사용할 모델
        # Form에서 사용할 모델의 속성
        fields = ['title', 'body', 'one_source', 'information_source']

        labels = {
            'title': '제목',
            'body': '내용',
            'one_source': '출처명',
            'information_source': '출처링크',
        }