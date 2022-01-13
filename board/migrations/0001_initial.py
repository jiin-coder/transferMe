# Generated by Django 3.0.3 on 2022-01-12 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='관련 데이터 번호')),
                ('title', models.CharField(max_length=200, verbose_name='제목')),
                ('body', models.TextField(verbose_name='내용')),
                ('one_source', models.TextField(verbose_name='출처명')),
                ('information_source', models.TextField(verbose_name='출처링크')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='content_type_post', to='contenttypes.ContentType')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
    ]