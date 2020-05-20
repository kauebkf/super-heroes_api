from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import HeroSerializer, HeroDetailSerializer
from core.models import Hero, User
from rest_framework.authentication import TokenAuthentication
from heroes.permissions import UpdateOwnHeroOnly

class HeroViewSet(viewsets.ModelViewSet):
    """Viewset for Hero model"""
    serializer_class = HeroSerializer
    queryset = Hero.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnHeroOnly,)

    def calculate_ratings(self):
        for hero in Hero.objects.all():
            hero.rating = hero.user_set.count()
            hero.save()
            hero.refresh_from_db()

    def get_queryset(self):
        """returns apropriate queryset"""


        return self.queryset

    def get_serializer_class(self):
        """Returns apropriate serializer class"""
        if self.action == 'retrieve':
            self.calculate_ratings()
            return HeroDetailSerializer

        return self.serializer_class

class MarvelViewSet(HeroViewSet):
    """Viewset for Marvel heroes"""
    queryset = Hero.objects.filter(universe='Marvel')


class DCViewSet(HeroViewSet):
    """Viewset for Marvel heroes"""
    queryset = Hero.objects.filter(universe='DC')
