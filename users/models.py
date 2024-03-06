from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):

    email = models.EmailField(max_length=60, unique=True)
    groups = models.ManyToManyField(Group, related_name='auth_user')
    user_permissions = models.ManyToManyField(Permission, related_name='auth_user')
