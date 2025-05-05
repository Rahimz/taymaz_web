from django.urls import path
from . import views


app_name = 'generals'

urlpatterns = [
    path('catalogue/', views.CatalogueView, name='catalogue'),
]
