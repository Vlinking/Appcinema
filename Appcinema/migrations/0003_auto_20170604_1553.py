# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-04 13:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Appcinema', '0002_auto_20170604_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'free'), (1, 'tentative booked'), (2, 'booked')], default=0)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Appcinema.Movie')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Appcinema.Seat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='screening',
            name='movie',
        ),
        migrations.DeleteModel(
            name='Screening',
        ),
    ]
