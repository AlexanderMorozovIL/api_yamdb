from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenView, SignView, UserViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', SignView.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
]
