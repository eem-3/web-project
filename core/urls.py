from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.view_home, name='home'),
    path('project/new/', views.PostCreateProject.as_view(), name='project_create'),

    path('project/<uuid:pk>/', views.EntityView1, name='project_detail'),
    path('media/<uuid:pk>/', views.EntityView1, name='media_detail'),
    path('my-content/', views.MyEntitiesView.as_view(), name='my_entities'),
    path('project/edit/<uuid:pk>/', views.PostUpdateProject.as_view(), name='project_edit'),
    path('project/delete/<uuid:pk>/', views.PostDeleteProject.as_view(), name='project_delete'),
    
     # Ruta de la API (Backend)
    path('api/tags/', views.api_tags_list, name='api_tags_list'),
    
    # Ruta de la Web (Frontend)
    path('tags-view/', views.lista_tags_frontend, name='tags_frontend'),
]