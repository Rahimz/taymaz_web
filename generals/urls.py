from django.urls import path
from django.views.generic.base import RedirectView
from . import views


app_name = 'generals'

urlpatterns = [
    path('catalogue/', views.CatalogueView, name='catalogue'),
    path('', RedirectView.as_view(pattern_name='generals:catalogue')),
]
