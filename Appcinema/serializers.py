from rest_framework import serializers

from Appcinema.models import Movie, Reservation


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    """
    Movie serializer.
    """
    class Meta:
        model = Movie
        fields = ('id', 'title',)



class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Reservation serializer.
    """
    class Meta:
        model = Reservation
        fields = ('seat', 'user', 'movie', 'status')