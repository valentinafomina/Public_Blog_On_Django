from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from .forms import CommentForm, CreateArticleForm
from .models import ArticleCategory, Article, Comment


class ArticlesView(ListView):
    model = Article
    ordering = 'published_date'
    paginate_by = 10
    template_name = 'mainapp/articles.html'
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


@method_decorator(csrf_exempt, name='dispatch')
class ArticleView(DetailView):
    model = Article
    template_name = 'mainapp/article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['title'] = 'Habr'
        context['categories'] = ArticleCategory.objects.all()
        context['form'] = CommentForm()
        comments = self.get_comments()
        context['comments'] = comments
        # context['user'] = self.request.User
        return context

    def get_comments(self):
        comments = Comment.objects.filter(article__pk=self.kwargs['pk'])
        return comments

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        context['form'] = form

        if form.is_valid():
            text = form.cleaned_data['text']
            author = self.request.user
            article = self.get_object()
            comments = self.get_comments()

            comment = Comment.objects.create(author=author, article=article, text=text)
            comment.save()

            form = CommentForm()
            context['form'] = form
            context['comments'] = comments
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


def create_article(request):

    article_create_form = CreateArticleForm(request.POST)
    context = {'article_create_form': article_create_form}

    if request.method == "POST":

        if article_create_form.is_valid():

            new_article = article_create_form.save(commit=False)
            new_article.user = request.user
            new_article.entryTime = datetime.now()
            new_article.save()
        return render(request, 'mainapp/articles.html', context)

    else:
        return render(request, 'mainapp/create_article.html', context)
