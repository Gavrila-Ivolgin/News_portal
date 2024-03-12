from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from news.models import Author


class IndexView(TemplateView):
    template_name = 'news/index.html'
    title = 'Good Elephant'


class NewsListViews(ListView):
    model = Author
    template_name = 'news/index.html'
    title = 'Список новостей'

    """
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        queryset = queryset.filter(category_id=category_id) if category_id else queryset
        return queryset.order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListViews, self).get_context_data()
        # Кеш категорий
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context
    """
