#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter, ModelMultipleChoiceFilter
from django.forms import DateTimeInput
from .models import Post, Category


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='added_at',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%m-%d-%Y %H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    """
    # Пример фильтра для выбора категории из выпадающего списка
    
    category = ModelChoiceFilter(
        field_name='postcategory__categoriesThrough',
        queryset=Category.objects.all(),
        label='Категории',
        empty_label='Все'
    )
    """
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__categoriesThrough',
        queryset=Category.objects.all(),
        label='Категории',
        conjoined=True,  # Для выбора только указанных категорий (союз - "и"), False = or
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }


class NewPostFilter(FilterSet):
    # title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            # ['text', 'added_at']
        }
