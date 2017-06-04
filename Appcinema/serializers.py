from rest_framework import serializers

from Appcinema.models import Movie, Reservation, Row, Seat


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    """
    Movie serializer.
    """
    class Meta:
        model = Movie
        fields = ('id', 'title',)


class RowSerializer(serializers.ModelSerializer):
    """
    Row serializer.
    """
    class Meta:
        model = Row
        fields = ('name',)


class SeatSerializer(serializers.ModelSerializer):
    """
    Seat serializer.
    """
    row = RowSerializer(read_only=True)
    class Meta:
        model = Seat
        fields = ('number', 'row')


class ReservationSerializer(serializers.ModelSerializer):
    """
    Reservation serializer.
    """
    seat = SeatSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = ('seat', 'user', 'movie', 'status')
