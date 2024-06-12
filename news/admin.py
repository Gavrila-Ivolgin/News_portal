from django.contrib import admin
from news.models import Post, Category, PostCategory, Subscription

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Subscription)

# Register your models here.

