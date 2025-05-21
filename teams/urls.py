from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
    path('create/', views.team_create, name='team_create'),
    path('<int:team_id>/add-member/', views.add_member, name='add_member'),
    path('<int:team_id>/remove-member/<int:user_id>/', views.remove_member, name='remove_member'),
]