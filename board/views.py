from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import resolve
from django.utils import timezone

import board
from accounts.models import User
from .forms import ArticleWriteForm, CommentForm
from .models import Article, Comment

from django.contrib import messages

@login_required(login_url='accounts:signin')
def comment_delete_article(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.writer:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('board:detail', article_id=comment.article.id)
    else:
        comment.delete()
    return redirect('board:detail', question_id=comment.article.id)


@login_required(login_url='accounts:signin')
def comment_modify_article(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.writer:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('board:detail', article_id=comment.article.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.update_date = timezone.now()
            comment.save()
            return redirect('board:detail', article_id=comment.article.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)


@login_required(login_url='accounts:signin')
def comment_create_article(request, article_id):

    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.writer = request.user
            comment.reg_date = timezone.now()
            comment.article = article
            comment.save()
            return redirect('board:detail', article_id=article.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)

@login_required(login_url='account:signin')
def vote_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user == article.writer:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        article.voter.add(request.user)
    return redirect('board:detail', article_id=article.id)


@login_required(login_url='accounts:signin')
def article_delete(request: HttpRequest, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user != article.writer:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:detail', article_id=article.id)
    article.delete()
    messages.success(request, "글이 삭제되었습니다.")
    return redirect('board:list')


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

    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        articles = Article.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-reg_date')
    elif so == 'popular':
        articles = Article.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-reg_date')
    else:  # recent
        articles = Article.objects.order_by('-reg_date')

    # 검색
    if kw:
        articles = Article.objects.filter(
            Article(title__icontains=kw) |
            Article(body__icontains=kw) |
            Article(one_source__icontains=kw) |
            Article(information_source__icontains=kw) |
            Article(writer__icontains=kw)
        ).distinct()

    # 페이징처리
    paginator = Paginator(articles, 1000) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'articles': page_obj, 'page': page, 'kw': kw, 'so': so}

    return render(request, 'board/article_list.html', context)


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
