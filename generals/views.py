from django.shortcuts import render

from .models import Catalogue

def CatalogueView(request):
    catalogue = Catalogue.objects.prefetch_related('images').all().last()
    context = dict(
        page_title = 'Catalogue',
        catalogue=catalogue
        
    )
    return render(
        request,
        'generals/catalogue.html',
        context
    )