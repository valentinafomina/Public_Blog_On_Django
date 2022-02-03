from django.core.management.base import BaseCommand

from mainapp.models import ArticleCategory, Article, Comment
from authapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        User.objects.all().delete()
        User.objects.create_superuser('admin', 'django@geekshop.local', '123', first_name='Nekr')
        _user = User.objects.get(first_name='Nekr')

        categories = ['Дизайн', 'Веб-разработка', 'Мобильная разработка', 'Маркетинг']

        ArticleCategory.objects.all().delete()
        for category in categories:
            new_category = ArticleCategory.objects.create(name=category)
            new_category.save()

        Article.objects.all().delete()
        Comment.objects.all().delete()
        for i in categories:
            for j in range(20):
                category_name = i
                _category = ArticleCategory.objects.get(name=category_name)
                new_article = Article.objects.create(user=_user,
                                                     title=f'test {i} / {j}',
                                                     article_text='test'*20,
                                                     category=_category
                                                     )
                new_article.save()
                for _ in range(5):
                    article = new_article
                    author = _user
                    text = 'test' * 10
                    Comment.objects.create(article=article,
                                           author=author,
                                           text=text
                                           )





