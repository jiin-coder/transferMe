from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ArticleForm
from .models import Article

def Article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {'article': article}
    return render(request, 'board/article_detail.html', context)

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
