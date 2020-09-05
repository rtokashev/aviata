from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('skypicker/', views.skypicker_flights_search, name='skypicker')
]
