from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
import board
from accounts.models import User

class Article(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자", related_name='writer_article')
    title = models.CharField(max_length=200, verbose_name="제목")
    body = models.TextField(verbose_name="내용")
    one_source = models.CharField(max_length=200, verbose_name="출처명")
    information_source = models.CharField(max_length=200, verbose_name="출처링크", blank=True)
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    voter = models.ManyToManyField(User, related_name='voter_article')  # 추천인 추가

    def __str__(self):
        return self.title




