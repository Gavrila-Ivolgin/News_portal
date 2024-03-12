from django.db import models
from django.db.models import Sum

from django.contrib.auth.models import User
# from users.models import User


class Author(models.Model):
    """
    Модель, содержащая объекты всех авторов.
    """
    # Связь «один-к-одному» с встроенной моделью пользователей User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_rating(self):
        """
        Обновляет рейтинг текущего автора на основе критериев:
        суммарный рейтинг каждой статьи автора умножается на 3;
        суммарный рейтинг всех комментариев автора;
        суммарный рейтинг всех комментариев к статьям автора.
        """

        # Суммарный рейтинг каждой статьи автора умножается на 3
        article_rating = self.posts.aggregate(total_rating=Sum('rating'))['total_rating'] or 0
        article_rating *= 3

        # Суммарный рейтинг всех комментариев автора
        comment_rating = self.user.comments.aggregate(total_rating=Sum('rating'))['total_rating'] or 0

        # Суммарный рейтинг всех комментариев к статьям автора
        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(total_rating=Sum('rating'))[
                                  'total_rating'] or 0

        # Обновление рейтинга автора
        self.rating = article_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return f'Автор: {self.user.username} | Рейтинг: {self.rating}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'Категория: {self.name}'


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
        """Увеличивает рейтинг поста на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг поста на единицу."""
        self.rating -= 1
        self.save()

    def preview(self):
        """Ограничивает вывод поля text."""
        preview_length = 124
        if len(self.text) <= preview_length:
            return self.text
        else:
            return self.text[:preview_length] + '...'

    def __str__(self):
        """Используем обратную связь self.categories.all() для получения
        всех связанных объектов Category для данного Post."""
        category_names = ', '.join(category.name for category in self.categories.all())
        return f'Автор: {self.author.user.username} | Категории: {category_names} | Тип: {self.get_type_display()} | ' \
               f'Заголовок: {self.title} | Рейтинг: {self.rating}'


class PostCategory(models.Model):
    """
    Промежуточная модель для связи «многие ко многим» между моделями Post и Category.
    Позволяет связать несколько категорий с каждой записью Post, а также обеспечивает
    дополнительные возможности и атрибуты для управления этой связью.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def like(self):
        """Увеличивает рейтинг комментария на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг комментария на единицу."""
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'Post: {self.post} | user: {self.user.username} | rating: {self.rating}'
