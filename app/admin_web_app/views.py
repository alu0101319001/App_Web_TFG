# admin_web_app/views.py
from django.shortcuts import render, get_object_or_404
from .models import Computer

def base_page(request):
    return render(request, 'base.html')

def main_page(request):
    computers = Computer.objects.all()
    return render(request, 'main_page.html', {'computers': computers})

def testing_page(request):
    computers = Computer.objects.all()
    return render(request, 'testing_page.html', {'ordenadores': computers})

def index(request):
    computers = Computer.objects.all()
    return render(request, 'computers/index.html', {'computers': computers})

def computer_detail(request, computer_id):
    computer = get_object_or_404(Computer, id=computer_id)
    return render(request, 'computers/computer_detail.html', {'computer': computer})
