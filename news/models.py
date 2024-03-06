from django.db import models
from django.db.models import Sum

from users.models import User


class Author(models.Model):
    """
    Модель, содержащая объекты всех авторов.
    """
    # Связь «один-к-одному» с встроенной моделью пользователей User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_set = None
        self.comment_set = None

    def update_rating(self):
        """Обновляет рейтинг текущего автора."""
        article_rating = self.post_set.aggregate(Sum('rating'))['rating__sum'] or 0
        comment_rating = self.comment_set.aggregate(Sum('rating'))['rating__sum'] or 0
        comment_rating_to_posts = self.comment_set.filter(post__author=self).aggregate(Sum('rating'))[
                                      'rating__sum'] or 0

        self.rating = (article_rating * 3) + comment_rating + comment_rating_to_posts
        self.save()

    def __str__(self):
        return f'Автор: {self.user.username} | Рейтинг: {self.rating}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    ARTICLE = 'article'
    NEWS = 'news'

    TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField()

    def like(self):
        """Увеличивает рейтинг на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг на единицу."""
        self.rating -= 1
        self.save()

    def preview(self):
        preview_length = 124
        if len(self.text) <= preview_length:
            return self.text
        else:
            return self.text[:preview_length] + '...'


class PostCategory(models.Model):
    """
    Промежуточная модель для связи «многие ко многим» между моделями Post и Category.
    Позволяет связать несколько категорий с каждой записью Post, а также обеспечивает
    дополнительные возможности и атрибуты для управления этой связью.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def like(self):
        """Увеличивает рейтинг на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг на единицу."""
        self.rating -= 1
        self.save()
