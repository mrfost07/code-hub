from django.urls import path
from . import views, api

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('<uuid:task_id>/', views.task_detail, name='task_detail'),
    path('create/', views.task_create, name='task_create'),
    path('project/<uuid:project_id>/create/', views.create_project_task, name='create_project_task'),
    path('<uuid:task_id>/update/', views.task_update, name='task_update'),
    path('task/<uuid:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task/<uuid:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('api/tasks/<uuid:task_id>/update-status/', views.update_task_status, name='update_task_status'),
    path('<uuid:task_id>/update-status/', views.update_task_status, name='update_task_status'),
]