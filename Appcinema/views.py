from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework import viewsets

from Appcinema.serializers import MovieSerializer
from Appcinema import models


@login_required
def home(request):
    return render(request, 'home.html')


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lists all movies.
    """
    queryset = models.Movie.objects.all()
    serializer_class = MovieSerializer
