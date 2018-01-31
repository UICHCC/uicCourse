from django.shortcuts import render
from . import models


def index(request):
    article = models.Article.objects.all()
    return render(request, 'index.html', {'articles': article})


def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'post.html', {'article': article})


def edit_page(request):
    return render(request, 'edit.html')


def edit_page_db(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    models.Article.objects.create(title=title, content=content)
    article = models.Article.objects.all()
    return render(request, 'index.html', {'articles': article})

