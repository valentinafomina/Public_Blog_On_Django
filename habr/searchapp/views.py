from django.db.models import Q
from django.shortcuts import render
from django.views import View
from itertools import chain
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from mainapp.models import Article, ArticleCategory
from authapp.models import User


class SearchList(View):
    template_name = 'searchapp/search_results.html'
    paginate_by = 100

    def get(self, request, *args, **kwargs):
        context = {}

        q = request.GET.get('search')
        context['search_name'] = q
        if q:
            query_sets = []

            # Поиск по статьям
            query_sets.append(Article.objects.search(query=q))
            # Поиск по пользователям
            query_sets.append(User.objects.search(query=q))
            # Поиск по категориям статей
            query_sets.append(ArticleCategory.objects.search(query=q))

            # Объединение в один
            final_set = list(chain(*query_sets))

            current_page = Paginator(final_set, 100)

            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(current_page.num_pages)

        return render(request=request, template_name=self.template_name, context=context)
