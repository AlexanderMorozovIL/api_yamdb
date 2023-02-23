'''РЕВЬЮ'''


import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Класс, фильтрующий различные поля модели."""

    year = django_filters.NumberFilter(field_name='year')
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(field_name='name')

    class Meta:
        model = Title
        fields = ['year', 'genre', 'category', 'name']
