# news/views
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse

from .filters import PostFilter
from news.forms import PostFormNews

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from .models import Subscription, Category, Post
from django.core.cache import cache
import logging
from django.utils.translation import gettext as _  # импортируем функцию для перевода
from common.views import TitleMixin

logger = logging.getLogger(__name__)
project_name = "Good Elephant"


class IndexView(TitleMixin, TemplateView):
    template_name = 'index.html'
    title = 'ГЕОГРАФИЯ-24'


class PostsList(ListView):
    model = Post  # queryset = Post.objects.all()
    ordering = "-dateCreation"
    template_name = "news/posts.html"
    context_object_name = "news"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = Post.objects.count()  # Передаем в шаблон общее количество новостей из модели.
        return context


class PostDetail(DetailView):
    model = Post  # queryset = Post.objects.get(pk=pk)
    template_name = "news/post.html"
    context_object_name = "new"

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'new-{self.kwargs["pk"]}', None)
        # Ели объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'new-{self.kwargs["pk"]}', obj)
        return obj


class PostsSearchList(ListView):
    model = Post  # queryset = Post.objects.all()
    ordering = "-dateCreation"
    template_name = "news/posts_search.html"
    context_object_name = "news"
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации, self.request.GET содержит объект QueryDict.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом
        # добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = Post.objects.count()  # Передаем в шаблон общее количество новостей из модели.
        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации.
        return context


class PostNewsCreate(PermissionRequiredMixin, CreateView):
    # raise_exception = True  # Выдача ошибки с 403 кодом для не авторизированных пользователей
    permission_required = ('news.add_post',)
    form_class = PostFormNews
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostFormNews
    model = Post
    template_name = 'news/post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news:posts_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')

    print("Category.objects.all().query =", Category.objects.all().query)

    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)


def open_html_page_about(request):
    txt = f'{project_name} | О нас'
    context = {'title': txt}
    return render(request, 'about.html', context)


def open_html_page_contact(request):
    txt = f'{project_name} | Контакты'
    context = {'title': txt}
    return render(request, 'contact.html', context)
