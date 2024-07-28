from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    TYPE = (
        (1, 'Танки'),
        (2, 'Хилы'),
        (3, 'ДД'),
        (4, 'Торговцы'),
        (5, 'Гилдмфстеры'),
        (6, 'Квестиверы'),
        (7, 'Кузнецы'),
        (8, 'Кожевники'),
        (9, 'Зульевары'),
        (10, 'Мастера заклинаний'),
    )

    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    category = models.CharField(max_length=8, choices=TYPE, default=1)
    upload = models.FileField(upload_to='uploads/')


class UserResponse(models.Model):  # Модель отклика
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class NewUser(User):
    status = models.BooleanField(default=False)
    auth_code = models.CharField(max_length=128)
