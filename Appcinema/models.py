from django.db import models


class Movie(models.Model):
    """
    Model class for the movie.
    """
    title = models.CharField(max_length=100)


class Screening(models.Model):
    """
    Model class for the movie screening.
    """
    movie = models.ForeignKey('Movie')


class Seat(models.Model):
    """
    Model class for the seat.
    """
    number = models.IntegerField(max_length=2)


class Row(models.Model):
    """
    Model class for the row of seats.
    """
    name = models.CharField(max_length=1)