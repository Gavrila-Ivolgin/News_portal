#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.models import User
from .models import PostCategory, Post, Author


@receiver(m2m_changed, sender=Post)  # PostCategory
def product_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        print('Создана запись PostCategory =', instance)
        print('instance.categories.through.id =', instance.categories.through.id)  # id Category
        print('instance.post.through.id =', instance.post.through.id)  # id Post

        emails = User.objects.filter(
            subscriptions__category=instance.categories.through.id
        ).values_list('email', flat=True)
        print('emails =', emails)

        queryset = Post.objects.filter(id=instance.post.through.id)
        queryset_author_id = queryset.values('author_id')  # <QuerySet [{'author_id': 2}]>
        author = queryset_author_id[0]['author_id']  # 2
        author = Author.objects.get(id=author)

        title_queryset = queryset.values('title')  # <QuerySet [{'author_id': 2, 'title': 'Прибытие в Крск'}]>
        title = title_queryset[0]['title']
        subject = f'Новый пост: {instance.categories.through}'  # Новый пост: Категория: Автомобиль

        text_content = (
            f'Автор: {author}\n'
            f'Заголовок: {title}\n\n'
            f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Автор: {author}<br>'
            f'Заголовок: {title}<br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Ссылка на пост</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@receiver(post_save, sender=PostCategory)
def product_created(instance, created, **kwargs):
    if not created:
        return
    else:
        print('Создана запись PostCategory =', instance)
        print('instance.categoriesThrough.id =', instance.categoriesThrough.id)  # id Category
        print('instance.postThrough.id =', instance.postThrough.id)  # id Post

    emails = User.objects.filter(
        subscriptions__category=instance.categoriesThrough.id
    ).values_list('email', flat=True)
    print('emails =', emails)

    queryset = Post.objects.filter(id=instance.postThrough.id)
    queryset_author_id = queryset.values('author_id')  # <QuerySet [{'author_id': 2}]>
    author = queryset_author_id[0]['author_id']  # 2
    author = Author.objects.get(id=author)

    title_queryset = queryset.values('title')  # <QuerySet [{'author_id': 2, 'title': 'Прибытие в Крск'}]>
    title = title_queryset[0]['title']
    subject = f'Новый пост: {instance.categoriesThrough}'  # Новый пост: Категория: Автомобиль

    text_content = (
        f'Автор: {author}\n'
        f'Заголовок: {title}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Автор: {author}<br>'
        f'Заголовок: {title}<br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
