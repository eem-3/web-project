from django.contrib import admin
from django.urls import include, path

from core.views import SignUpView, view_home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # name='signup' -> used in nav bar: {% url 'signup' %}
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', view_home, name='home'),
    path('', view_home, name='home'),
    #path('', include('core.urls')),
]