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
    path('sync-list/', views.sync_list, name='sync_list'),
    path('execute-command/', views.execute_command, name='execute_command'),
    path('run-sh-script/', views.run_sh_script, name='run_sh_script'),
    path('toggle-warning/<int:computer_id>/', views.toggle_warning, name='toggle_warning'),
    path('toggle-exam-mode/<int:computer_id>/', views.toggle_exam_mode, name='toggle_exam_mode'),
    path('activate-exam-mode/', views.activate_exam_mode, name='activate_exam_mode'),
    path('deactivate-exam-mode/', views.deactivate_exam_mode, name='deactivate_exam_mode'),
    path('update-exam-mode/', views.update_exam_mode, name='update_exam_mode'),
    path('turn-on-computer/<int:computer_id>/', views.turn_on_computer, name='turn_on_computer'),
    path('turn-off-computer/<int:computer_id>/', views.turn_off_computer, name='turn_off_computer'),
    path('upgrade-computer/<int:computer_id>/', views.upgrade_computer, name='upgrade_computer')
]

