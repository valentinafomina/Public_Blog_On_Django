from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, QuerySet, Q
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from authapp.models import User
from .forms import CommentForm, CreateArticleForm
from .models import ArticleCategory, Article, Comment


class AuthorTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author


class BanTestMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_banned


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
        queryset = super(ArticlesView, self).get_queryset().order_by('-created_date')
        queryset = queryset.filter(is_published=True, is_banned=False)
        if 'pk' in self.kwargs:
            if self.kwargs['pk'] == 0:
                return queryset
            elif self.kwargs['pk'] != 0:
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
        context['same_articles'] = self.get_same_articles()
        return context

    def get_comments(self):
        comments = Comment.objects.filter(article__pk=self.kwargs['pk'])
        return comments

    def get_same_articles(self):
        if self.object.tags:
            same_articles = None
            for tag in self.object.tags.all():
                same_tag_articles = tag.tagged_articles.all().annotate(cnt=Count('likes'))
                if same_articles:
                    same_articles = same_articles.union(same_tag_articles)
                else:
                    same_articles = same_tag_articles
        else:
            category = self.object.category
            same_articles = self.model.objects.filter(category=category).annotate(cnt=Count('likes'))

        return same_articles.order_by('-cnt')[:5]


@method_decorator(csrf_exempt, name='dispatch')
class ArticleCreateView(LoginRequiredMixin, BanTestMixin, CreateView):
    model = Article
    template_name = 'mainapp/create_article.html'
    form_class = CreateArticleForm
    pk = None
    login_url = '/auth/login/'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        self.object = article
        self.pk = article.pk
        self.object.create_tags()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('mainapp:article', kwargs={'pk': self.pk})


@method_decorator(csrf_exempt, name='dispatch')
class ArticleUpdateView(LoginRequiredMixin, AuthorTestMixin, UpdateView):
    model = Article
    template_name = 'mainapp/create_article.html'
    form_class = CreateArticleForm
    pk = None
    login_url = '/auth/login/'

    def get_success_url(self):
        return reverse_lazy('mainapp:article', kwargs={'pk': self.pk})

    def form_valid(self, form):
        self.object.create_tags()
        self.pk = self.object.pk
        return super(ArticleUpdateView, self).form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, AuthorTestMixin, DeleteView):
    model = Article
    login_url = '/auth/login/'
    success_url = reverse_lazy('mainapp:articles')

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.is_published:
            self.object.is_published = False
        else:
            self.object.is_published = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


def about_us(request):
    title = 'о нас'
    content = {'title': title}

    return render(request, 'mainapp/about_us.html', content)


class CommentView(LoginRequiredMixin, BanTestMixin, View):
    def post(self, request, pk, *args, **kwargs):
        form = CommentForm(request.POST)
        article = Article.objects.get(pk=pk)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.article = article
            new_comment.save()

            comments = Comment.objects.filter(article=article).order_by('-created_at')
            context = {
                'article': article,
                'form': form,
                'comments': comments,
            }
            return HttpResponseRedirect(reverse('mainapp:article', kwargs={'pk': article.pk}))


class CommentReplyView(LoginRequiredMixin, BanTestMixin, View):
    def post(self, request, article_pk, pk, *args, **kwargs):
        article = Article.objects.get(pk=article_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.article = article
            new_comment.parent = parent_comment
            new_comment.save()

        comments = Comment.objects.filter(article=article).order_by('-created_at')
        context = {
            'article': article,
            'form': form,
            'comments': comments,
        }
        return HttpResponseRedirect(reverse('mainapp:article', kwargs={'pk': article_pk}))


class LikeSwitcher(LoginRequiredMixin, BanTestMixin, View):
    login_url = '/auth/login/'

    def handle_no_permission(self):
        self.request.path = self.request.path.replace('/like', '')
        return super(LikeSwitcher, self).handle_no_permission()

    def post(self, request, model, pk, *args, **kwargs):
        models = {
            'Article': Article,
            'Comment': Comment,
            'User': User,
        }
        is_liked = False
        model_to_liked = models[model].objects.get(pk=pk)
        for like in model_to_liked.likes.all():
            if like == request.user:
                is_liked = True
                break
        if is_liked:
            model_to_liked.likes.remove(request.user)
        else:
            model_to_liked.likes.add(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
