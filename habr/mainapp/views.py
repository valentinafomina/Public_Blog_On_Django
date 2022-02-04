from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime

from .forms import CommentForm, CreateArticleForm
from .models import ArticleCategory, Article, Comment


class ArticlesView(ListView):
    model = Article
    ordering = '-created_date'
    paginate_by = 100
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


@method_decorator(csrf_exempt, name='dispatch')
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'mainapp/create_article.html'
    form_class = CreateArticleForm
    pk = None
    login_url = '/authenticate/login/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        self.object = instance
        self.pk = instance.id
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('mainapp:article', kwargs={'pk': self.pk})



