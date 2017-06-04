from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    """
    Model class for the movie.
    """
    title = models.CharField(max_length=100)


class Row(models.Model):
    """
    Model class for the row of seats.
    """
    name = models.CharField(max_length=1)


class Seat(models.Model):
    """
    Model class for the seat.
    """
    number = models.IntegerField()
    row = models.ForeignKey('Row')


class Reservation(models.Model):
    """
    Model class for booking a seat on a movie.
    """
    STATUS_FREE = 0
    STATUS_TENTATIVE_BOOKED = 1
    STATUS_BOOKED = 2
    STATUS_CHOICES = (
        (STATUS_FREE, 'free'),
        (STATUS_TENTATIVE_BOOKED, 'tentative booked'),
        (STATUS_BOOKED, 'booked'),
    )

    seat = models.ForeignKey('Seat')
    user = models.ForeignKey(User)
    movie = models.ForeignKey('Movie')
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_FREE)

