from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from accounts.models import User


class Comment(models.Model):
    class Meta:
        ordering = ['-id']

    reg_date = models.DateTimeField('등록일자', auto_now_add=True)
    update_date = models.DateTimeField('갱신일자', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    content_type = models.ForeignKey(ContentType, related_name="content_type_comment", on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField('관련 데이터 번호')
    content_object = GenericForeignKey('content_type', 'object_id')
    body = models.TextField(verbose_name="댓글내용")
