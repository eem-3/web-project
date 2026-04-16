from django.contrib import admin
from django.urls import path
from core.views import view_home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_home, name='home'),
    path('home/', view_home, name='home'),

]
from django.urls import include, path

from core.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # name='signup' -> used in nav bar: {% url 'signup' %}
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
]
