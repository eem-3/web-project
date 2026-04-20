from django.urls import path
from . import views
from .views import APIMediaDetail, APIEntityDetail, APIProjectDetail, APIEntityList
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.view_home, name='home'),


    ### API URLs ###
    path('api/status/', views.APIStatusList.as_view(), name='status-list'),
    path('api/status/<int:pk>/', views.APIStatusDetail.as_view(), name='status-detail'),

    path('api/tags/', views.APITagList.as_view(), name='tag-list'),
    path('api/tags/<uuid:pk>/', views.APITagDetail.as_view(), name='tag-detail'),


    path('api/entities/', views.APIEntityList.as_view(), name='entity-list'),
    path('api/entities/<uuid:pk>/', views.APIEntityDetail.as_view(), name='entity-detail'),
    path('api/media/<uuid:pk>/', views.APIMediaDetail.as_view(), name='media-detail'),
    path('api/projects/<uuid:pk>/', views.APIProjectDetail.as_view(), name='project-detail'),
]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'xml'])