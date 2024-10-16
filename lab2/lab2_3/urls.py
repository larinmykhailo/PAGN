from django.urls import path

from .src.Util import initPoints
from .views import index, plot_2_3, plot_2_5, add_point

# initPoints()

urlpatterns = [
    path('', index, name='index'),
    path('plot_2_3', plot_2_3, name='plot_2_3'),
    path('plot_2_5', plot_2_5, name='plot_2_5'),
    path('add_point', add_point, name='add_point')
]
