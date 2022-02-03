from django.contrib import admin
from .models import Article, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

admin.site.register(Comment)

@admin.register(Article)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ('body', )
    list_display = (
        'writer',
        'title',
        'body',
        'one_source',
        'information_source'
    )
    list_display_links = list_display
    search_fields = [

        'writer',
        'title',
        'body',
        'one_source',
        'information_source'
    ]

