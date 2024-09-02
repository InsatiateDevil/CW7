from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='email',
        help_text='Введите ваш email'
    )
    phone_number = models.CharField(
        max_length=25,
        verbose_name='телефон',
        help_text='Введите ваш номер телефона',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='аватар',
        help_text='Выберите аватар',
        blank=True,
        null=True
    )
    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Город',
        blank=True,
        null=True
    )
    telegram_chat_id = models.CharField(
        max_length=25,
        verbose_name='Чат ID пользователя',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email
