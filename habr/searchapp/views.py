from django.shortcuts import render
from django.views import View
from itertools import chain
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from mainapp.models import Article
from authapp.models import User

class SearchList(View):
    template_name = 'searchapp/search_results.html'

    def get(self, request, *args, **kwargs):
        context = {}

        q = request.GET.get('search')
        context['search_name'] = q
        if q:
            query_sets = []

            # Поиск по статьям
            query_sets.append(Article.objects.filter(title__contains=q))
            query_sets.append(Article.objects.filter(article_text__contains=q))

            # Поиск по пользователям
            query_sets.append(User.objects.filter(username__contains=q))
            query_sets.append(User.objects.filter(first_name__contains=q))
            query_sets.append(User.objects.filter(last_name__contains=q))

            # Поиск по категориям
            # query_sets.append(Article.objects.filter(category__contains=q))

            # Объединение в один
            final_set = list(chain(*query_sets))

            current_page = Paginator(final_set, 10)

            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(current_page.num_pages)

        return render(request=request, template_name=self.template_name, context=context)
