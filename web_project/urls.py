from django.contrib import admin
from django.urls import path
from core.views import view_home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_home, name='home'),
    path('home/', view_home, name='home'),

]
