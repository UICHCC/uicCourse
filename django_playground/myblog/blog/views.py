from django.shortcuts import render
from . import models


def index(request):
    article = models.Article.objects.all()
    return render(request, 'index.html', {'articles': article})


def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'post.html', {'article': article})


def edit_page(request, article_id):
    if  str(article_id) == '0':
        return render(request, 'edit.html')
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'edit.html', {'article': article})


def edit_page_db(request):
    article_id = request.POST.get('article_id', '0')
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    if article_id == '0':
        models.Article.objects.create(title=title, content=content)
        article = models.Article.objects.all()
        return render(request, 'index.html', {'articles': article})

    modify_article = models.Article.objects.get(pk=article_id)
    modify_article.title = title
    modify_article.content = content
    modify_article.save()
    return render(request, 'post.html', {'article': modify_article})