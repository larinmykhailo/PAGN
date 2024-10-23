from django.urls import path

from .views import index, plot_view_before, plot_view_after, add_point

urlpatterns = [
    path('', index, name='index'),
    path('add_point', add_point, name='add_point'),
    path('plot_view_before', plot_view_before, name='plot_view_before'),
    path('plot_view_after', plot_view_after, name='plot_view_after'),
]
