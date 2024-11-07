from django.urls import path

from .views import index, plot1, add_point1, calculate, compare_results

urlpatterns = [
    path('', index, name='index'),
    path('add_point1', add_point1, name='add_point1'),
    path('plot1', plot1, name='plot1'),
    path('calculate', calculate, name='calculate'),
    path('compare_results', compare_results, name='compare_results'),
]
