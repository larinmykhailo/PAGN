from django.urls import path

from .views import index, plot_2_3, add_point


urlpatterns = [
    path('', index, name='index'),
    path('plot_2_3', plot_2_3, name='plot_2_3'),
    path('add_point', add_point, name='add_point')
]
