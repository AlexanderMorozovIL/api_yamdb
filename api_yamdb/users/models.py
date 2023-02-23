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

        '''это свойство унаследовано от AbstractUser, при чем, унаследованное свойство более универсально и красивое, для этого стоит взглянуть на исходный код.
https://github.com/django/django/blob/main/django/contrib/auth/models.py
'''
        unique=True,
        max_length=settings.USERNAME_MAX_LENGTH,

        '''идея супер, но в исходном коде цифра нас устраивала.
'''
        validators=(validate_username,),

        '''что бы сохранить красоту поля first_name при наследовали модели юзера.
делаем валидацию на me в clean методе модели, но не забудьте использовать super() что бы не потерять унаследованную функциональность:
https://docs.djangoproject.com/en/4.1/ref/models/instances/#django.db.models.Model.clean
https://github.com/django/django/blob/main/django/contrib/auth/models.py
'''
        null=False,

        '''В большинстве случаев, эта настройка для текстовых полей не ставится.
Подробнее в доке.
https://docs.djangoproject.com/en/4.1/ref/models/fields/#null
Так же для текстовых и часовых типов полей эта настройка не нужна
https://stackoverflow.com/questions/8609192/what-is-the-difference-between-null-true-and-blank-true-in-django
'''
        blank=False,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH,
        null=False,

        '''поле гмейла должно быть обязательно, делая так ты делаешь его не обязательным, и модель стерилизатор будет это учитывать.
'''
        blank=False,
        verbose_name='Электронный адрес почты',
        help_text='Введите email'
    )
    first_name = models.CharField(

        '''фирстнейм и ластнейм аналогично юзернейму'''
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

        '''излишняя сложность, укажем цифру с запасом на будущие роли и успокоимся.
'''
        verbose_name='Роль пользователя',
        help_text='Укажите роль пользователя'
    )
    confirmation_code = models.CharField(

        '''опять же лучше генерировать токен используя from django.contrib.auth.tokens import default_token_generator
так же этот инструмент позволит гораздо проще проверить этот токен при получении джвт токена
и в этом случае можно будет отказаться от хранения этого токена в модели юзера, что будет более правильным решением, а так этот токен по сути лишние байты в базе данных.
смысла хранить его нет.
'''
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXXXX'
    )

    '''добавим мета класс модели с русскими именами и вариацией на уникальность поля юзернейма и емейла.
'''

    def __str__(self):
        return str(self.username)

        '''а поле юзернейма числовое чтоль?+)
нам не нужно тут стр.
'''

    @property

    '''Это можно убрать и считать по умолчанию всех юзерами, а в моментах где необходимы повышенные привелегии проверять соответствующими методами.
'''
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
