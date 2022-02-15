from django.urls import path

from searchapp.views import SearchList

app_name = 'search'

urlpatterns = [
    path('search/', SearchList.as_view(), name='search_result'),
]