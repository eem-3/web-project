from django.contrib import admin
from django.urls import include, path

from core.views import SignUpView, view_home, EntityView1
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from core.forms import BootstrapLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=BootstrapLoginForm,
    ), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
