from rest_framework import serializers
from reviews.models import Category, Genre, Title
from users.models import User
from users.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для User."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        """Валидация имени пользователя."""
        return validate_username(value)


class NotAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для User не админ."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class SignSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрции."""

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title
