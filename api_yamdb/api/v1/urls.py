from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenView, ReviewViewSet, SignView, TitleViewSet,
                    UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

auth_urlpatterns = [
    path('signup/', SignView.as_view(), name='signup'),
    path('token/', GetTokenView.as_view(), name='get_token'),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urlpatterns)),
]
