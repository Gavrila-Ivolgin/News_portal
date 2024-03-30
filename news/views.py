from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from news.models import Post


class NewsList(ListView):
    model = Post  # queryset = Post.objects.all()
    ordering = "-dateCreation"
    template_name = "news/news.html"
    context_object_name = "news"


class NewDetail(DetailView):
    model = Post  # queryset = Post.objects.get(pk=pk)
    template_name = "news/new.html"
    context_object_name = "new"
