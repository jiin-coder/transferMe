from django.contrib import admin
from .models import Article
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(Article)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents', )
    list_display = (
        'title',
        'body',
        'one_source',
        'information_source'
    )
    list_display_links = list_display