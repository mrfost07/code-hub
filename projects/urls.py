from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<uuid:project_id>/', views.project_detail, name='project_detail'),
    path('<uuid:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('<uuid:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('<uuid:project_id>/kanban-board/', views.kanban_board, name='kanban_board'),
]