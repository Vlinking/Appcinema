from django.shortcuts import render

# Create your views here.


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView

from rest_framework import viewsets

from Appcinema.serializers import MovieSerializer
from Appcinema import models


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
class ChooseMovieView(CreateView):
    """
    View for choosing the movie.
    """
    template_name = 'choose_movie.html'


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lists all movies.
    """
    queryset = models.Movie.objects.all()
    serializer_class = MovieSerializer
