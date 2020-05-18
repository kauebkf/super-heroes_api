from core import serializers
from core.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from core.permissions import UpdateOwnProfileOnly
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

app_name = 'user'

class UserProfileViewSet(viewsets.ModelViewSet):
    """For creating and updating profiles"""
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfileOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginView(ObtainAuthToken):
    """Creates user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
