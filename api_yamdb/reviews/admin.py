from django.contrib import admin

from .models import Category, Genre, Title, Review, Comments, TitleGenre


admin.site.register(Category)
'''REVIEW'''
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comments)
admin.site.register(TitleGenre)
