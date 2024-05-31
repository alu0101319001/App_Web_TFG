# admin_web_app/views.py
from django.shortcuts import render
from .models import Computer

def base_page(request):
    return render(request, 'base.html')

def main_page(request):
    return render(request, 'main_page.html')

def testing_page(request):
    computers = Computer.objects.all()
    return render(request, 'testing_page.html', {'ordenadores': computers})
