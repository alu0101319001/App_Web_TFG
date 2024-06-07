# backend/admin_web_project_dj/admin_web_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('computer_detail/<int:computer_id>/', views.computer_detail, name='computer_detail'),
    path('base_page/', views.base_page, name='base_page'),
    path('testing_page/', views.testing_page, name='testing_page'),
    path('main_page/', views.main_page, name='main_page'),
    path('turn-on-all/', views.turn_on_all, name='turn_on_all'),
    path('turn-off-all/', views.turn_off_all, name='turn_off_all'),
    path('update-view/', views.update_view, name='update_view'),  # Cambiado de 'update/' a 'update-view/'
]

