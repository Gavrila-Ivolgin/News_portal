from django.urls import path
from news.views import PostsList, PostDetail, PostsSearchList, PostNewsCreate, PostUpdate, PostDelete

app_name = 'news'

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('search/', PostsSearchList.as_view(), name='posts_search'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostNewsCreate.as_view(), name='post_news_created'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
