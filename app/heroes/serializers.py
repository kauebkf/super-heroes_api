from rest_framework import serializers
from core import models


class HeroSerializer(serializers.ModelSerializer):
    """Serializer for Hero object"""

    class Meta:

        model = models.Hero
        fields = ('id', 'alias', 'alter_ego')
