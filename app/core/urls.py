from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views

app_name = 'user'

router = DefaultRouter()
router.register('user', views.UserProfileViewSet, base_name='user')

urlpatterns = [
    path('user/login/', views.UserLoginView.as_view()),
    path('', include(router.urls))
]
