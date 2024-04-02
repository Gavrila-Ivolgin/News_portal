#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_filters
from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
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

    category = ModelChoiceFilter(
        field_name='postcategory__categoriesThrough',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все'
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
