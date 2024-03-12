from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        """
        Обновляет рейтинг текущего автора на основе критериев:
        суммарный рейтинг каждой статьи автора умножается на 3;
        суммарный рейтинг всех комментариев автора;
        суммарный рейтинг всех комментариев к статьям автора.
        """
        # Суммарный рейтинг каждой статьи автора умножается на 3
        post_rating = self.post_set.aggregate(postRating=Sum("rating"))['postRating'] or 0
        post_rating *= 3

        # Суммарный рейтинг всех комментариев автора
        comment_rating = self.authorUser.comments.aggregate(commentRating=Sum('rating'))['commentRating'] or 0

        # Суммарный рейтинг всех комментариев к статьям автора
        post_comment_rating = Comment.objects.filter(commentPost__author__authorUser=self).aggregate(
            postCommentRating=Sum('rating'))['postCommentRating'] or 0

        # Обновление рейтинга автора
        self.ratingAuthor = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        pass
        # return f'Автор: {self.user.username} | Рейтинг: {self.rating}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    # def __str__(self):
    #     return f'Категория: {self.name}'


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    CATEGORY_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # related_name='posts'
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

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
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoriesThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)  # related_name='comments'
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

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
