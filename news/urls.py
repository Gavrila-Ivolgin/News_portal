from django.urls import path
from news.views import NewsList, NewDetail

app_name = 'news'

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewDetail.as_view()),
]
