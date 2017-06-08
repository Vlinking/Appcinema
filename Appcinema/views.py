from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.views import APIView

from Appcinema.models import Row, Seat
from Appcinema.serializers import MovieSerializer, ReservationSerializer, ReservationSimplerSerializer
from Appcinema import models


class HomeView(LoginRequiredMixin, TemplateView):
    """
    View for displaying the main view.
    Also preloads the seat display grid.
    """
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        """
        Preload the seat display grid layout.
        """
        data = {"rows": {}}
        rows = Row.objects.all()
        for row in rows:
            data["rows"][row] = Seat.objects.filter(row=row)
        return TemplateResponse(request, self.template_name, data)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lists all movies.
    """
    queryset = models.Movie.objects.all()
    serializer_class = MovieSerializer

    @detail_route()
    def reservation_list(self, request, pk=None):
        movie = self.get_object()
        reservation = models.Reservation.objects.filter(movie=movie)
        reservation_json = ReservationSerializer(reservation, many=True)
        return Response(reservation_json.data)


class ReservationViewSet(viewsets.ModelViewSet):
    """
    The all purpose viewset for manipulating reservations. Magic goes on here.
    """
    queryset = models.Reservation.objects.all()
    serializer_class = ReservationSimplerSerializer
    permission_classes = (IsAuthenticated,)


class ConfirmReservation(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        We have confirmed all of our reservations in a batch.
        """
        seats = models.Seat.objects.filter(
            row=models.Row.objects.get(name=request.data['row']),
            number__in=request.data['seats'].split(","),
        )
        reservations = models.Reservation.objects.filter(
            seat__in=seats,
            movie=request.data['movie'],
            user=request.user
        )
        for reservation in reservations:
            reservation.status = models.Reservation.STATUS_BOOKED
            reservation.save()

        return Response([], status=status.HTTP_200_OK)




