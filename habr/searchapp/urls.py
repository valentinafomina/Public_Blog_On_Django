from django.urls import path

from searchapp.views import SearchArticleList, SearchUserList

app_name = 'search'

urlpatterns = [
    path('search/articles', SearchArticleList.as_view(), name='search_article_result'),
    # path('search/users', SearchUserList.as_view(), name='search_user_result'),
]