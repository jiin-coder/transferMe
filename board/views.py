from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import ArticleForm


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
    return render(request, 'board/create.html', {'form': form})
