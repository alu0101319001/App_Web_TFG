# admin_web_app/views.py
from django.shortcuts import render

def base_page(request):
    return render(request, 'base.html', {})

def testing_page(request):
    ordenadores = [
        {'nombre': 'Ordenador 1', 'estado': 'encendido'},
        {'nombre': 'Ordenador 2', 'estado': 'apagado'},
        # Añade más ordenadores según sea necesario
    ]
    return render(request, 'testing_page.html', {'ordenadores': ordenadores})
