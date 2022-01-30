from django.views.generic import ListView, DetailView

from .forms import CommentForm
from .models import ArticleCategory, Article, Comment


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

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['title'] = 'Habr'
        context['categories'] = ArticleCategory.objects.all()
        context['comment'] = CommentForm()
        comments = self.get_comments()
        context['comments'] = comments
        return context

    def get_comments(self):
        comments = Comment.objects.filter(article=self.kwargs['pk'])
        return comments

    def post(self, request, *args, **kwargs):
        pass


def create_article():
    return None