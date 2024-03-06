from django.urls import path
from news.views import NewsListViews

app_name = 'news'

urlpatterns = [
    path('', NewsListViews.as_view(), name='index'),
]
