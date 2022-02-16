from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

from comments.forms import CommentForm
from .forms import ArticleWriteForm
from .models import Article, Comment

from django.contrib import messages


@login_required
def comment_delete(request: HttpRequest, article_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        raise exceptions.PermissionDenied()

    comment.delete()

    messages.success(request, "댓글이 삭제되었습니다.")

    return redirect("board:article_detail", article_id=article_id)


def comment_modify(request: HttpRequest, article_id, comment_id):
    article = get_object_or_404(Article, id=article_id)
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            messages.success(request, "댓글이 수정되었습니다.")
            return redirect("board:article_detail", article_id=article_id)
    else:
        form = CommentForm(None, instance=comment)

    context = {
        "article": article,
        "comment": comment,
        "CommentForm": form,
    }

    return render(request, "board/comment_modify.html", context)


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


def article_detail(request: HttpRequest, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_type = ContentType.objects.get_for_model(article)
            comment.object_id = article.id
            comment.user = request.user
            comment.save()
            messages.success(request, "댓글이 등록되었습니다.")

            return redirect("board:article_detail", article_id=article.id)
    else:
        form = CommentForm()

        form.errors

    comments = article.comments.select_related('user').order_by('-id')
    context = {
        "article": article,
        "comments": comments,
        "CommentForm": form,
    }

    return render(request, 'board/article_detail.html', context)


def comment_create(request: HttpRequest, article_id):
    return article_detail(request, article_id)


def article_list(request: HttpRequest):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    kws = kw.split(' ')

    articles = Article.objects.all().order_by('-id').distinct()

    # 검색
    if kw:
        articles = articles \
            .filter(tag_set__name__in=kws)

    # 페이징처리
    paginator = Paginator(articles, 1000)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(kw)
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
