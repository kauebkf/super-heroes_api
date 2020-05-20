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

    def get_queryset(self):
        """returns apropriate queryset"""
        queryset = self.queryset
        top = bool(
            int(self.request.query_params.get('top', 0))
        )
        if top:
             queryset = queryset.filter().order_by('rating').reverse()[:1]

        return queryset


    def calculate_ratings(self):
        """Calculates ratings based on amount of users"""
        for hero in Hero.objects.all():
            hero.rating = hero.user_set.count()
            hero.save()
            hero.refresh_from_db()

    def get_serializer_class(self):
        """Returns apropriate serializer class"""
        self.calculate_ratings()
        if self.action == 'retrieve':
            return HeroDetailSerializer

        return self.serializer_class

class MarvelViewSet(HeroViewSet):
    """Viewset for Marvel heroes"""
    queryset = Hero.objects.filter(universe='Marvel')



class DCViewSet(HeroViewSet):
    """Viewset for Marvel heroes"""
    queryset = Hero.objects.filter(universe='DC')
