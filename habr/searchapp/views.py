from django.db.models import Q
from django.shortcuts import render
from django.views import View
from itertools import chain
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView

from mainapp.models import Article, ArticleCategory
from authapp.models import User


class SearchArticleList(ListView):
    model = Article
    paginate_by = 100
    template_name = 'searchapp/search_article_results.html'
    extra_context = {
        'title': 'Habr',
        'categories': ArticleCategory.objects.all(),
    }

    def get_context_data(self, **kwargs):
        context = context = super(SearchArticleList, self).get_context_data(**kwargs)

        q = self.request.GET.get('search')
        sort = self.request.GET.getlist('sort')
        context['search_name'] = q
        if q:

            queryset = Article.objects.filter(Q(title__icontains=q.capitalize()) | Q(title__icontains=q.lower())
                                        | Q(title__icontains=q.upper()) | Q(article_text__icontains=q.capitalize())
                                        | Q(article_text__icontains=q.lower()) | Q(article_text__icontains=q.upper()))

            if sort:
                queryset = queryset.order_by(*sort)
            else:
                queryset.order_by('-likes')

            context['articles'] = queryset

        return context


class SearchUserList(ListView):
    model = User
    paginate_by = 100
    template_name = 'searchapp/search_user_results.html'
    extra_context = {
        'title': 'Habr',
    }

    def get_context_data(self, **kwargs):
        context = context = super(SearchUserList, self).get_context_data(**kwargs)

        q = self.request.GET.get('search')
        sort = self.request.GET.getlist('sort')
        context['search_name'] = q
        if q:

            queryset = User.objects.filter(
                Q(username__icontains=q.capitalize()) | Q(username__icontains=q.lower())
                | Q(username__icontains=q.upper()) | Q(first_name__icontains=q.capitalize())
                | Q(first_name__icontains=q.lower()) | Q(first_name__icontains=q.upper())
                | Q(last_name__icontains=q.lower()) | Q(last_name__icontains=q.upper())
                | Q(last_name__icontains=q.lower())
            )

            if sort:
                queryset = queryset.order_by(*sort)

            context['users'] = queryset

        return context
