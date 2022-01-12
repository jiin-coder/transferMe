from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
class Board(models.Model):
    object_id = models.PositiveIntegerField('관련 데이터 번호')
    writer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=200, verbose_name="제목")
    body = models.TextField(verbose_name="내용")
    one_source = models.TextField(verbose_name="출처명")
    information_source = models.TextField(verbose_name="출처링크")
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    content_type = models.ForeignKey(ContentType, related_name="content_type_post", on_delete=models.DO_NOTHING)
    content_object = GenericForeignKey('content_type', 'object_id')