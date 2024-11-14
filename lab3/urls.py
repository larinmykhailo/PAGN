from django.urls import path

from .views import index, plot1, compare_results, add_point1, unclassified_results, all_results

urlpatterns = [
    path('', index, name='index'),
    path('add_point1', add_point1, name='add_point1'),
    path('plot1', plot1, name='plot1'),
    path('compare_results', compare_results, name='compare_results'),
    path('unclassified_results', unclassified_results, name='unclassified_results'),
    path('all_results', all_results, name='all_results'),
]
