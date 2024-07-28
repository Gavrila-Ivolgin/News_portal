from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from news.views import IndexView, subscriptions, open_html_page_about, open_html_page_contact
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

    path('about/', open_html_page_about, name='about'),
    path('contact/', open_html_page_contact, name='contact'),

]

if settings.DEBUG:
    # urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
