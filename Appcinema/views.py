from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        Do custom things here and create the table row.
        """
        modified_data = request.data.copy()
        modified_data['user'] = request.user.id
        modified_data['status'] = models.Reservation.STATUS_TENTATIVE_BOOKED
        row = Row.objects.get(name=modified_data['row'])
        seat = Seat.objects.get(number=modified_data['seat'], row=row)
        modified_data['seat'] = seat.id
        # check if the instance already exists, we don't reference it by id
        # so create always goes in
        try:
            instance = models.Reservation.objects.get(
                seat=modified_data['seat'],
                user=modified_data['user'],
                movie=modified_data['movie'],
                status=modified_data['status']
            )
        except models.Reservation.DoesNotExist:
            instance = None

        if instance:
            modified_data['status'] = 1 - models.Reservation.STATUS_FREE
            modified_data['id'] = instance.id
            serializer = self.get_serializer(instance, data=modified_data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        else:
            serializer = self.get_serializer(data=modified_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)








