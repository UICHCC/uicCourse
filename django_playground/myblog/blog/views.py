from django.shortcuts import render
from . import models


def index(request):
    article = models.Article.objects.all()
    return render(request, 'index.html', {'article': article})




