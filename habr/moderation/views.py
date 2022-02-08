from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView

from mainapp.models import Article
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

    def get_queryset(self):
        queryset = super(ModeratorPage, self).get_queryset().order_by('-banned_on')
        return queryset


@permission_required('moderation.view_report', raise_exception=True)
def reports(request):
    return render(request, 'moderation/mod_page.html')


# @permission_required('moderation.change_article', raise_exception=True)
def ban_article(request, pk):
    article = Article.objects.get(id=pk)
    if article.is_banned == False:
        article.is_banned = True
        article.save()

        ban = BannedObjects.create(object_pk=article, user=request.user)
        ban.save()

        return redirect('moderation:moderator_page')
    else:
        return redirect('moderation:moderator_page')


def unban_article(request, pk):
    object = BannedObjects.objects.get(id=pk)

    article = Article.objects.get(id=object.banned_object_id)
    article.is_banned=False
    article.save()

    object.delete()

    return redirect('/')




