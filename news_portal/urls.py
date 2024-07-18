from django.contrib import admin
from django.urls import include, path
from news.views import IndexView, subscriptions
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('news/', include('news.urls', namespace='news')),
    path('articles/', include('articles.urls', namespace='articles')),
    path("accounts/", include("allauth.urls")),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
