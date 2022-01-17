from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

import board
from .forms import ArticleForm
from .models import Article

from django.contrib import messages

@login_required(login_url='accounts:signin')
def article_modify(request, article_id):

    article = get_object_or_404(Article, pk=article_id)
    if request.user != board.writer:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:detail', article_id=article.id)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.update_date = timezone.now()  # 수정일시 저장
            article.save()
            return redirect('board:detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    context = {'form': form}
    return render(request, 'board/article_form.html', context)

def Article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'board/article_detail.html', {'article': article})

def Article_list(request):
    articles = Article.objects.all().order_by('-id')
    return render(request, 'board/article_list.html', {"articles": articles})

def Article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.writer = request.user
            article.reg_date = timezone.now()
            article.save()
            return redirect('main')
    else:
        form = ArticleForm()
    return render(request, 'board/article_create.html', {'form': form})
