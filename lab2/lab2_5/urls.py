from django.urls import path
from .views import index, plot

urlpatterns = [
    path('', index, name='index'),
    path('plot', plot, name='plot'),
]
