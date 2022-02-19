from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView

from authapp.models import User
from mainapp.models import Article, Comment
from .models import BannedObjects


class ModeratorPage(ListView):
    model = BannedObjects
    ordering = '-banned_on'
    paginate_by = 100
    template_name = 'moderation/mod_page.html'
    context_object_name = 'banned_objects'

    extra_context = {
        'title': "Список заблокированных вами объектов",
        'banned_object_name': Article.title,
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = BannedObjects.objects.all().filter(
            banned_comment=None, banned_by=self.request.user)
        context['comment_list'] = BannedObjects.objects.all().filter(
            banned_article=None, banned_by=self.request.user)
        context['reported_articles'] = Report.objects.all().filter(
            reported_comment=None, is_active=True).order_by('-reported_on')
        return context


def report_article(request, pk):
    article = Article.objects.get(id=pk)

    if request.method == 'POST':
        text = request.POST['text']

        if '@moderator' in text:
            report = Report.create(object_pk=article, user=request.user)
            print(f'object_pk: {article} user: {request.user}')
            report.save()
            return HttpResponseRedirect('/')
        else:
            print('wrong!')
    return HttpResponseRedirect(request.path_info)


def mute_report(request, pk):
    if request.user.is_staff:
        object = Report.objects.get(id=pk)
        object.is_active = False
        object.save()
    return HttpResponseRedirect(request.path_info)


def ban_article(request, pk):
    if request.user.is_staff:
        article = Article.objects.get(id=pk)
        if not article.is_banned:
            article.is_banned = True
            article.save()

            ban = BannedObjects.create(object_pk=article, user=request.user)
            ban.save()

            return redirect('moderation:moderator_page')
        else:
            return redirect('moderation:moderator_page')


def unban_article(request, pk):
    if request.user.is_staff:
        object = BannedObjects.objects.get(id=pk)

        article = Article.objects.get(id=object.banned_article_id)
        article.is_banned = False
        article.save()

        object.delete()

        return redirect('/')


def ban_comment(request, pk):
    if request.user.is_staff:
        comment = Comment.objects.get(id=pk)
        if not comment.is_banned:
            comment.is_banned = True
            comment.save()

            ban = BannedObjects.create(object_pk=comment, user=request.user)
            ban.save()

            return redirect('moderation:moderator_page')
        else:
            return redirect('moderation:moderator_page')


def unban_comment(request, pk):
    if request.user.is_staff:
        object = BannedObjects.objects.get(id=pk)

        comment = Comment.objects.get(id=object.banned_comment)
        comment.is_banned = False
        comment.save()

        object.delete()

        return redirect('/')


def change_moderator_status(request, pk):
    if request.user.is_superuser:
        user = User.objects.get(id=pk)
        if not user.is_staff:
            user.is_staff = True
            user.save()
            return redirect('/')
        elif user.is_staff:
            user.is_staff = False
            user.save()
            return redirect('/')
    else:
        return HttpResponseRedirect(request.path_info)


# def ban_comment(request, pk):
#     comment = Comment.objects.get(id=pk)
#     if not comment.is_banned:
#         comment.is_banned = True
#         comment.save()
#
#     ban = BannedObjects.create(object_pk=comment, user=request.user)
#     ban.save()
#
#     return HttpResponseRedirect('/')
#

