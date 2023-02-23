import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Нельзя использовать имя пользователя me.

    '''по пеп-257 многострочный докстринг состоит из:
1) строки сводки
2) дополнительного описания
между ними ставится одна пустая строка.
'''
    Допускается использовать только буквы, цифры и символы.
    """

'''В функциях после докстринга пустая строка не ставится. PEP-257.
https://www.python.org/dev/peps/pep-0257/#id5
'''
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$')

    if pattern.fullmatch(value) is None:
        match = re.split(pattern, value)
        symbol = ''.join(match)
        raise ValidationError(f'Некорректные символы в username: {symbol}')
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
    return value
