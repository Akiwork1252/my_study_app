from django.db import models
from django.contrib.auth.models import AbstractUser


# カスタムユーザー
class CustomUser(AbstractUser):
    interests = models.ManyToManyField('ascension.InterestCategory', 
                                       through='ascension.UserInterest',
                                       related_name='users')

    class Meta:
        verbose_name_plural = 'CustomUser'
