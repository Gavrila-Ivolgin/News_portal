from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from news.models import Post
from articles.forms import PostFormArticles


class PostArticleCreate(CreateView):
    form_class = PostFormArticles
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostFormArticles
    model = Post
    template_name = 'news/post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news:posts_list')
