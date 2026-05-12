from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.view_home, name='home'),
    path('project/new/', views.PostCreateProject.as_view(), name='project_create'),

    path('project/<uuid:pk>/', views.EntityView1, name='project_detail'),
    path('media/<uuid:pk>/', views.EntityView1, name='media_detail'),
]