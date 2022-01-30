from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView

from .forms import CreateArticleForm
from .models import ArticleCategory, Article


def index(request):
    pass


class ArticlesView(ListView):
    model = Article
    ordering = 'published_date'
    paginate_by = 10
    template_name = 'mainapp.articles.html'
    context_object_name = 'articles'
    extra_context = {
        'title': 'Habr',
        'categories': ArticleCategory.objects.all(),
    }

    def get_queryset(self):
        queryset = super(ArticlesView, self).get_queryset()
        if 'pk' in self.kwargs:
            if self.kwargs['pk'] == 0:
                return queryset
            elif self.kwargs['pk'] == 1:
                queryset = queryset.filter(category_id__pk=self.kwargs['pk'])
                return queryset
        else:
            return queryset


class ArticleView(DetailView):
    model = Article
    template_name = 'mainapp.article.html'
    context_object_name = 'article'
    extra_context = {
        'title': 'Habr',
        'categories': ArticleCategory.objects.all(),
    }


def create_article(request):

    article_create_form = CreateArticleForm(request.POST)
    context = {'article_create_form': article_create_form}

    if request.method == "POST":

        if article_create_form.is_valid():

            new_article = article_create_form.save(commit=False)
            new_article.user = request.user
            new_article.entryTime = datetime.now()
            new_article.save()
        return HttpResponseRedirect('create_article')

    else:
        return render(request, 'mainapp/create_article.html', context)


