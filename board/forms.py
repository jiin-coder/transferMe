from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

from .models import Article


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
            'body': SummernoteWidget()
        }

        def clean(self):
            # pass2
            cleaned_data = super().clean()

            title = cleaned_data.get('title', '')
            body = cleaned_data.get('body', '')
            one_source = cleaned_data.get('one_source', '')
            information_source = cleaned_data.get('information_source', '')

            if title == '':
                self.add_error('title', '제목')
            elif body == '':
                self.add_error('body', '내용')
            elif one_source == '':
                self.add_error('one_source', '출처명')
            elif information_source == '':
                self.add_error('information_source', '출처링크')
            else:
                self.title = title
                self.body = body
                self.one_source = one_source
                self.information_source = information_source

