from django.urls import path
from search.views import results

urlpatterns = [
    path('results/', results, {'template_name': 'search/results.html'}, name='search_results'),
]

