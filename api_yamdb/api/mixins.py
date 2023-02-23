from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class ModelMixinSet(CreateModelMixin, ListModelMixin,
'''REVIEW'''
                    DestroyModelMixin, GenericViewSet):
    """Класс MixinSet для дальнейшего использования."""

    pass
'''REVIEW'''
