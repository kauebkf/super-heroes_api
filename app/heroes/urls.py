from django.urls import path, include
from rest_framework.routers import DefaultRouter

from heroes import views

app_name = 'hero'

router = DefaultRouter()
router.register('hero', views.HeroViewSet, base_name='hero')
router.register('marvel', views.MarvelViewSet, base_name='marvel')
router.register('dc', views.DCViewSet, base_name='dc')

urlpatterns = [
    path('', include(router.urls))
]
