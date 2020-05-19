from rest_framework import viewsets
from .serializers import HeroSerializer
from core.models import Hero

class HeroViewSet(viewsets.ModelViewSet):
    """Viewset for Hero model"""
    serializer_class = HeroSerializer
    queryset = Hero.objects.all()
