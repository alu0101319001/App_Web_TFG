# backend/admin_web_project_dj/admin_web_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('get-computer-details/<int:computer_id>/', views.get_computer_details, name='get_computer_details'),
    path('base_page/', views.base_page, name='base_page'),
    path('testing_page/', views.testing_page, name='testing_page'),
    path('main_page/', views.main_page, name='main_page'),
    path('turn-on-all/', views.turn_on_all, name='turn_on_all'),
    path('turn-off-all/', views.turn_off_all, name='turn_off_all'),
    path('run-scan/', views.run_scan, name='run_scan'), 
    path('execute-playbook/<str:playbook>/<str:hostname>/', views.execute_playbook, name='execute_playbook'),
    path('copy-files/', views.copy_files, name='copy_files'),
    path('execute-command/', views.execute_command, name='execute_command'),
    path('run-sh-script/', views.run_sh_script, name='run_sh_script'),
]

