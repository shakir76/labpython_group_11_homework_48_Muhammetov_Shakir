from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name="Аватар")
    profile_github = models.URLField(max_length=200, null=True, blank=True, verbose_name='Ссылка на профиль')
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name="Описание")
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь",
                                related_name="profile")
