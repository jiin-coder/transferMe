from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import resolve
from django.utils import timezone

import board
from accounts.models import User
from .forms import ArticleWriteForm
from .models import Article

from django.contrib import messages


@login_required(login_url='accounts:signin')
def article_modify(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user != article.writer:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', article_id=article.id)

    if request.method == "POST":
        form = ArticleWriteForm(request.POST, instance=article)

        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            messages.success(request, "글이 수정되었습니다.")
            return redirect("board:detail", article_id=article_id)
    else:
        form = ArticleWriteForm(None, instance=article)
    return render(request, 'board/article_write.html', {'form': form})





def Article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'board/article_detail.html', {'article': article})


def Article_list(request):
    articles = Article.objects.all().order_by('-id')
    return render(request, 'board/article_list.html', {"articles": articles})


def Article_write(request):
    if request.method == 'POST':
        form = ArticleWriteForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.writer = request.user
            article.save()
            return redirect('board:detail', article.id)
    else:
        form = ArticleWriteForm()
    context = {'form': form}
    return render(request, 'board/article_write.html', context)
