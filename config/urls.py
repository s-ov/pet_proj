from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('users.urls', 'users'), namespace='users')),
    path('substation/', include(('substation.urls', 'substation'), namespace='substation')),
    path('mcc/', include(('mcc.urls', 'mcc'), namespace='mcc')),
    path('node/', include(('node.urls', 'node'), namespace='node')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
