from django.views.generic import ListView, DetailView


from habr.articleapp.models import Article, ArticleCategory


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


