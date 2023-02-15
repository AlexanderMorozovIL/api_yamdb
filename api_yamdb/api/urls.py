from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, GenreViewSet

app_name = 'api'


router_v1 = SimpleRouter()


router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router_v1.urls))
]
