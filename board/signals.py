#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
from .models import UserResponse


@receiver(post_save, sender=UserResponse)
def my_handler(sender, instance, created, **kwargs):
    if instance.status:
        mail = instance.author.email
        send_mail(
            'Subject here',
            'Here is the message',
            'host@mail.ru',
            [mail],
            fail_silently=False,
        )
    mail = instance.article.author.email
    send_mail(
        'Subject here',
        'Here is the message',
        'host@mail.ru',
        [mail],
        fail_silently=False,
    )



