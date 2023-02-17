from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title
from users.models import User
from .permissions import AdminOnly
from reviews.models import Category, Genre
from .serializers import (GetTokenSerializer,
                          NotAdminSerializer,
                          SignSerializer,
                          UserSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer
                          )
from .utils import get_confirmation_code, send_confirmation_code


class UserViewSet(ModelViewSet):
    """
    Вьюсет модели User.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnly]
    filter_backends = [SearchFilter]
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


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
        user.save()
        send_confirmation_code(user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    """
    Получение JWT-токена по confirmation code.
    """

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
                )
            }
        )


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
