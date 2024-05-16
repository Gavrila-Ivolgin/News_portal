# news/views
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse

from news.models import Post
from .filters import PostFilter
from news.forms import PostFormNews


class IndexView(TemplateView):
    template_name = 'news/index.html'
    title = 'Good Elephant'

    def get(self, request, *args, **kwargs):
        # Пример использования request и username
        if request.user.is_authenticated:
            username = request.user.username
            return HttpResponse(f'Привет, {username}!')
        else:
            return HttpResponse('Привет, незарегистрированный пользователь!')


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
