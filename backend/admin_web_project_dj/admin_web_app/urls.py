# backend/admin_web_project_dj/admin_web_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('testing_page/', views.testing_page, name='testing_page'),
]
    