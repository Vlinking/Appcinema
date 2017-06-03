from rest_framework import serializers

from Appcinema.models import Movie


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    """
    Movie serializer.
    """
    class Meta:
        model = Movie
        fields = ('title',)