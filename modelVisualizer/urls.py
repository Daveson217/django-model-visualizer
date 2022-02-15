from unicodedata import name
from django.urls import path
from .views import RelationalModelVisualizerView, get_database_model_data

urlpatterns = [
    path('', RelationalModelVisualizerView.as_view(), name='relational-model'),
    path('data/', get_database_model_data, name='get_database_model_data')
]