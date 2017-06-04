from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route

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

