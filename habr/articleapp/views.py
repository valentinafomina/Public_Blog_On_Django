from django.shortcuts import render
from datetime import datetime
from django.views.generic import CreateView

from .models import Article
from .forms import CreateArticleForm


def create_article(request):
    article_create_form = CreateArticleForm(request.POST)
    context = {'article_create_form': article_create_form}

    if request.method == "POST":

        if article_create_form.is_valid():


            new_article = article_create_form.save(commit=False)
            new_article.user = request.user
            new_article.entryTime = datetime.now()
            new_article.save()

        return render(request, 'articleapp/create_article.html', context)

    else:
        return render(request, 'articleapp/create_article.html', context)


