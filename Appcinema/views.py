from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from rest_framework import viewsets

from Appcinema.models import Row, Seat
from Appcinema.serializers import MovieSerializer
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
