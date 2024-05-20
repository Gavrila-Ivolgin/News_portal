#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.core.mail import EmailMultiAlternatives, mail_managers, mail_admins


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    # first_name = forms.CharField(label="Имя")
    # last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            # "first_name",
            # "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href=" https://b75d-78-36-117-197.ngrok-free.app/news">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email,
                                                             'nebosst@yandex.ru',
                                                             'Natveres@yandex.ru',
                                                             'gavrivolgin@gmail.com']
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте!'
        )

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте!'
        )

        return user
