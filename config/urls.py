from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView 


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        '', 
         TemplateView.as_view(template_name='index.html'), 
         name='main_page'
         ),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('substation/', include(('substation.urls', 'substation'), namespace='substation')),
    path('mcc/', include(('mcc.urls', 'mcc'), namespace='mcc')),
    path('node/', include(('node.urls', 'node'), namespace='node')),
    path('task/', include(('task.urls', 'task'), namespace='task')),
    path('assignments/', include(('assignments.urls', 'assignments'), namespace='assignments')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
