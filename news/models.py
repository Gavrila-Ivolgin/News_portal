from django.db import models
from users.models import User


class Author(models.Model):
    """
    Модель, содержащая объекты всех авторов.
    """
    # Связь «один-к-одному» с встроенной моделью пользователей User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = 0

    def update_rating(self):
        """
        Обновляет рейтинг текущего автора.
        :return:
        """
        """
        Он состоит из следующего:
            суммарный рейтинг каждой статьи автора умножается на 3;
            суммарный рейтинг всех комментариев автора;
            суммарный рейтинг всех комментариев к статьям автора.
        """


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    pass


class PostCategory(models.Model):
    pass


class Comment(models.Model):

    def like(self):
        """
        Увеличивает рейтинг на единицу.
        :return:
        """
        pass

    def dislike(self):
        """
        Уменьшает рейтинг на единицу.
        :return:
        """
        pass
