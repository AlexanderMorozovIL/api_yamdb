from django.contrib import admin

from .models import User

admin.site.register(User)

"""
тогда можно было бы подстроить вывод в админке.
"""
