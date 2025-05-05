from django.urls import path
from . import views


app_name = 'generals'

urlpatterns = [
    path('catalouge/', views.CatalougeView, name='catalouge'),
]
