from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ArticleWriteForm
from .models import Article

from django.contrib import messages


@login_required(login_url='account:signin')
def vote_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user == article.writer:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        article.voter.add(request.user)
    return redirect('board:article_detail', article_id=article.id)


@login_required(login_url='accounts:signin')
def article_delete(request: HttpRequest, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user != article.writer:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:article_detail', article_id=article.id)
    article.delete()
    messages.success(request, "글이 삭제되었습니다.")
    return redirect('board:list')


@login_required(login_url='accounts:signin')
def article_modify(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user != article.writer:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:article_detail', article_id=article.id)

    if request.method == "POST":
        form = ArticleWriteForm(request.POST, instance=article)

        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            messages.success(request, "글이 수정되었습니다.")
            return redirect("board:article_detail", article_id=article_id)
    else:
        form = ArticleWriteForm(None, instance=article)
    return render(request, 'board/article_write.html', {'form': form})


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'board/article_detail.html', {'article': article})


def article_list(request):

    articles = Article.objects.all().order_by('-id')

    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어

    # 검색
    if kw:
        articles = Article.objects.filter(
            Q(title__icontains=kw) | Q(body__icontains=kw) | Q(one_source__icontains=kw) | Q(
                information_source__icontains=kw) | Q(writer__username__icontains=kw)).distinct()

    # 페이징처리
    paginator = Paginator(articles, 1000)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'articles': page_obj, 'page': page, 'kw': kw}

    return render(request, 'board/article_list.html', context)


def article_write(request):
    if request.method == 'POST':
        form = ArticleWriteForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.writer = request.user
            article.save()
            return redirect('board:article_detail', article.id)
    else:
        form = ArticleWriteForm()
    context = {'form': form}
    return render(request, 'board/article_write.html', context)
