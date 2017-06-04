from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'api/movies', views.MovieViewSet)
router.register(r'api/reservation', views.ReservationViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomeView.as_view(), name='home'),
    # Django REST API bare view
    url(r'api/confirm_reservation', views.ConfirmReservation.as_view()),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    # Django REST API
    url(r'^', include(router.urls)),
]
