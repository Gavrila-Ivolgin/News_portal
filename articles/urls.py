from django.urls import path
from articles.views import PostArticleCreate
from news.views import PostUpdate, PostDelete

app_name = 'articles'

urlpatterns = [
    path('create/', PostArticleCreate.as_view(), name='post_article_created'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
