from django.urls import path

from .src.Util import initPoints
from .views import index, plot, add_point

initPoints()

urlpatterns = [
    path('', index, name='index'),
    path('plot', plot, name='plot'),
    path('add_point', add_point, name='add_point')
]
