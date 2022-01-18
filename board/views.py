from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

import board
from accounts.models import User
from .forms import ArticleWriteForm
from .models import Article

from django.contrib import messages

@login_required(login_url='accounts:signin')
def article_modify(request, article_id):

    article = get_object_or_404(Article, pk=article_id)

    if request.method == "POST":
        form = ArticleWriteForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.update_date = timezone.now()  # 수정일시 저장
            article.save()
            return redirect('board:detail', article_id=article.id)
    else:
        form = ArticleWriteForm(instance=article)
    context = {'form': form}
    return render(request, 'board/article_form.html', context)

def Article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'board/article_detail.html', {'article': article})

def Article_list(request):
    articles = Article.objects.all().order_by('-id')
    return render(request, 'board/article_list.html', {"articles": articles})

def Article_write(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }

    if request.method == 'GET':
        write_form = Article_write()
        context['forms'] = write_form
        return render(request, 'board/article_write.html', context)

    elif request.method == 'POST':
        write_form = ArticleWriteForm(request.POST)

        if write_form.is_valid():
            writer = User.objects.get(user_id=login_session)
            article = Article(
                title=write_form.title,
                body=write_form.body,
                one_source=write_form.one_source,
                information_source=write_form.information_source
            )
            article.save()
            return redirect('board:detail', article_id=article.id)
        else:
            context['forms'] = write_form
            if write_form.error:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/article_write.html', context)
