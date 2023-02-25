from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .mixins import CategoryGenreModelMixin, ModelViewSetWithoutPUT
from .permissions import (
    AdminModeratorAuthorReadOnly, AdminOnly,
    IsAdminOrReadOnly
)
from .serializers import (
    CategorySerializer, CommentsSerializer,
    GenreSerializer, GetTokenSerializer,
    NotAdminSerializer, ReviewSerializer, SignSerializer,
    TitleCreateSerializer, TitleGetSerializer,
    UserSerializer
)


class UserViewSet(ModelViewSetWithoutPUT):
    """
    Вьюсет модели User.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=NotAdminSerializer,
        url_path='me'
    )
    def get_current_user_info(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignView(APIView):
    """
    Регистрация нового пользователя.
    Отправка кода для подтверждения регистрации на email.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignSerializer(data=request.data, partial=True)
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            user, created = User.objects.get_or_create(
                username=request.data.get('username')
            )
            if created is False:
                confirmation_code = default_token_generator.make_token(user)
                user.confirmation_code = confirmation_code
                user.save()
                return Response('токен обновлен', status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(
            username=serializer.data['username'],
            email=request.data['email']
        )
        confirmation_code = default_token_generator.make_token(user)
        email = request.data.get('email')
        send_mail(
            'Код подтверждения',
            f'Ваш код: {confirmation_code}',
            from_email=None,
            recipient_list=[email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    """
    Получение JWT-токена по confirmation code.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            if User.objects.filter(username=username).exists():
                token = AccessToken.for_user(user)
                return Response(
                    {'token': str(token)},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ModelViewSetWithoutPUT):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = [
        AdminModeratorAuthorReadOnly,
    ]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSetWithoutPUT):
    """Вьюсет для комментариев."""

    serializer_class = CommentsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AdminModeratorAuthorReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(CategoryGenreModelMixin):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(CategoryGenreModelMixin):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Вьюсет для произведения."""

    queryset = Title.objects.select_related('category').annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleGetSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    search_fields = ['name']
    ordering_fields = ['name', 'year']

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleGetSerializer
        return TitleCreateSerializer
