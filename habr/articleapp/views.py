from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from django.views.generic.edit import FormView

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
            # article_create_form.remove()

        # return render(request, 'articleapp/create_article.html', context)
        return HttpResponseRedirect('create_article')

    else:
        return render(request, 'articleapp/create_article.html', context)


