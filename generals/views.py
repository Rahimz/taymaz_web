from django.shortcuts import render



def CatalougeView(request):
    context = dict(
        page_title = 'Catalouge'
        
    )
    return render(
        request,
        'generals/catalouge.html',
        context
    )