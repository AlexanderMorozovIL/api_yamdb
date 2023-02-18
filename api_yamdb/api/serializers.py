from rest_framework import serializers
from reviews.models import Review, Comments

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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )


class CommentsSerializer(serializers.ModelSerializer):
    """Сериалайзер для комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )
