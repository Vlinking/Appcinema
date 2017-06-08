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
        fields = ('id', 'number', 'row')


class ReservationSerializer(serializers.ModelSerializer):
    """
    Reservation serializer.
    """
    seat = SeatSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = ('seat', 'user', 'movie', 'status')


class ReservationSimplerSerializer(serializers.ModelSerializer):
    """
    A simpler reservation serializer for setting statuses.
    """
    class Meta:
        model = Reservation
        fields = ('seat', 'user', 'movie', 'status')
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        """
        Either create or update the reservation with a different status.
        """
        instance, created = Reservation.objects.get_or_create(
            seat=validated_data['seat'],
            user=self.context['request'].user,
            movie=validated_data['movie'],
            status=validated_data['status']
        )
        if not created:
            instance.status = validated_data['status']

        return instance




