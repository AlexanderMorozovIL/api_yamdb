from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import (AdminModeratorAuthorReadOnly, AdminOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, GetTokenSerializer,
                          NotAdminSerializer, ReviewSerializer, SignSerializer,
                          TitleSerializerCreate, TitleSerializerGet,
                          UserSerializer)
from .utils import get_confirmation_code, send_confirmation_code


class UserViewSet(ModelViewSet):
    '''REVIEW'''
    """
    Вьюсет модели User.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    '''REVIEW'''
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']
'''REVIEW'''

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        '''REVIEW'''
        if request.method == 'PATCH':
            if request.user.is_admin:
                '''REVIEW'''
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            '''REVIEW'''
        return Response(serializer.data)
        '''REVIEW'''


class SignView(APIView):
    """
    Регистрация нового пользователя.
    Отправка кода для подтверждения регистрации на email.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            '''REVIEW'''
            user, _ = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError as error:
            raise ValidationError(
                ('Ошибка при попытке создать новую запись '
                 f'в базе с username={username}, email={email}')
            ) from error
        user.confirmation_code = str(get_confirmation_code())
        '''REVIEW'''
        user.save()
        send_confirmation_code(user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    """
    Получение JWT-токена по confirmation code.
    """
    '''REVIEW'''

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(
                {
                    "confirmation_code": ("Неверный код доступа "
                                          f"{confirmation_code}")
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "token": str(
                    RefreshToken.for_user(user).access_token
                    '''REVIEW'''
                )
            }
        )


class ReviewViewSet(viewsets.ModelViewSet):
    '''REVIEW'''
    """Вьюсет для отзывов."""

    queryset = Review.objects.all()
    '''REVIEW'''
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    '''REVIEW'''
    permission_classes = [
        AdminModeratorAuthorReadOnly,
    ]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    '''REVIEW'''
    """Вьюсет для комментариев."""

    serializer_class = CommentsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AdminModeratorAuthorReadOnly
    ]

    def get_queryset(self):
        return Comments.objects.filter(
            '''REVIEW'''
            title=get_object_or_404(
                Title, pk=self.kwargs.get('title_id')),
            review=get_object_or_404(
                Review, pk=self.kwargs.get('review_id'))
        ).all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review, title=title)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(ModelMixinSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Вьюсет для произведения."""

    serializer_class = TitleSerializerGet
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        '''REVIEW'''
        filters.OrderingFilter
    ]
    filterset_class = TitleFilter
    search_fields = ['name']
    ordering_fields = ['name', 'year']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            '''REVIEW'''
            return TitleSerializerCreate
        return TitleSerializerGet

    def get_queryset(self):
        '''REVIEW'''
        queryset = Title.objects.all()
        '''REVIEW'''
        return queryset
