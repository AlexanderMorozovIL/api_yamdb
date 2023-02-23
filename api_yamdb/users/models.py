from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """
    Модель пользователя с дополнительными полями
    биография и роль.
    """

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    username = models.CharField(
        '''REVIEW'''
        unique=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        '''REVIEW'''
        validators=(validate_username,),
        '''REVIEW'''
        null=False,
        '''REVIEW'''
        blank=False,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH,
        null=False,
        '''REVIEW'''
        blank=False,
        verbose_name='Электронный адрес почты',
        help_text='Введите email'
    )
    first_name = models.CharField(
        '''REVIEW'''
        blank=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        verbose_name='Первоe имя пользователя',
        help_text='Введите первое имя'
    )
    last_name = models.CharField(
        blank=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        verbose_name='Фамилия пользователя',
        help_text='Введите фамилию'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография пользователя',
        help_text='Опишите свою биографию'
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        max_length=max((len(item) for _, item in ROLE_CHOICES)),
        '''REVIEW'''
        verbose_name='Роль пользователя',
        help_text='Укажите роль пользователя'
    )
    confirmation_code = models.CharField(
        '''REVIEW'''
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXXXX'
    )
    '''REVIEW'''

    def __str__(self):
        return str(self.username)
        '''REVIEW'''

    @property
    '''REVIEW'''
    def is_user(self):
        """Пользователь по умолчанию."""
        return self.role == User.USER

    @property
    def is_moderator(self):
        """Пользователь с правами модератора."""
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        """Пользователь с правами админа и суперпользователей."""
        return (
            self.role == User.ADMIN
            or self.is_superuser
        )
