from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from accounts.models import User
from comments.models import Comment
from tags.models import Tag
import re


class Article(models.Model):
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.title}, {self.body}, {self.one_source}, {self.information_source}"

    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자", related_name='writer_article')
    title = models.CharField(max_length=200, verbose_name="제목")
    body = models.TextField(verbose_name="내용")
    one_source = models.CharField(max_length=200, verbose_name="출처명")
    information_source = models.CharField(max_length=200, verbose_name="출처링크", blank=True)
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    voter = models.ManyToManyField(User, related_name='voter_article')  # 추천인 추가
    comments = GenericRelation(Comment, related_query_name="comment")
    tags = models.CharField(max_length=50, blank=True)
    tag_set = models.ManyToManyField(Tag, blank=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        old_tags = self.tag_set.all()
        new_tags = self.extract_tag_list()

        delete_tags:list[Tag] = []
        add_tags:list[Tag] = []

        for old_tag in old_tags:
            if not old_tag in new_tags:
                delete_tags.append(old_tag)

        for new_tag in new_tags:
            if not new_tag in old_tags:
                add_tags.append(new_tag)

        for delete_tag in delete_tags:
            self.tag_set.remove(delete_tag)

        for add_tag in add_tags:
            self.tag_set.add(add_tag)

    def extract_tag_list(self) -> list[Tag, ...]:
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.tags)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def summary(self):
        return self.body[:30]







