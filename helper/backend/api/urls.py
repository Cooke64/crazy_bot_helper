from django.urls import path, include, re_path
from rest_framework import routers

from .views.countries import CountryViewSet
from .views.document import DocumentViewSet
from .views.favorite_tg import FavoriteTgSerializerViewSet
from .views.tg_users import TelegramUsersViewSet

router = routers.DefaultRouter()

router.register('country', CountryViewSet, basename='country')
router.register('users', TelegramUsersViewSet, basename='users')
router.register('favorites', FavoriteTgSerializerViewSet, basename='favorites')
router.register('documents', DocumentViewSet, basename='documents')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
