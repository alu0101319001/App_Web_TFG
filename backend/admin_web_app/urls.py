# backend/admin_web_project_dj/admin_web_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('base_page/', views.base_page, name='base_page'),
    path('testing_page/', views.testing_page, name='testing_page'),
]
