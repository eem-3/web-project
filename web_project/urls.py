from django.contrib import admin
from django.urls import include, path

from core.views import SignUpView, view_home, EntityView1

from core.views import SignUpView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # provides accounts/login/ and accounts/logout/
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # name='signup' -> used in nav bar: {% url 'signup' %}
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', view_home, name='home'),
    path('', include('core.urls')),
    path('<uuid:pk>', EntityView1, name='Entity'),
]
