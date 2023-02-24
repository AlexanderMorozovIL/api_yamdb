from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, UpdateModelMixin,
                                   RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import status
from rest_framework.response import Response


class CategoryGenreModelMixin(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    """Класс MixinSet для категориев и жанров."""

    pass


class TitleModelMixin(
    CategoryGenreModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin
):
    """Класс MixinSet для категориев и жанров."""

    pass


class ModelViewSetWithoutPUT(
    ModelViewSet
    ):
    """Набор представлений допускает все методы, кроме PUT."""

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
