from django.urls import path
from news.views import NewsList, NewDetail, NewsSearchList

app_name = 'news'

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('search/', NewsSearchList.as_view(), name='news_search'),
    path('<int:pk>', NewDetail.as_view()),
]
