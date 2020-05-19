from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import HeroSerializer
from core.models import Hero
from rest_framework.authentication import TokenAuthentication
from heroes.permissions import UpdateOwnHeroOnly

class HeroViewSet(viewsets.ModelViewSet):
    """Viewset for Hero model"""
    serializer_class = HeroSerializer
    queryset = Hero.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnHeroOnly,)

class MarvelViewSet(HeroViewSet):
    """Viewset for Marvel heroes"""
    queryset = Hero.objects.filter(universe='Marvel')
