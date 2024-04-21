from django.contrib import admin
from news.models import Post, Category, PostCategory

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)

# Register your models here.

