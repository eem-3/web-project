from django.contrib import admin
from django.urls import include, path

from core.views import SignUpView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # provides accounts/login/ and accounts/logout/
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
