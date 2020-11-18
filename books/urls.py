from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home),
    path('upload', views.upload),
    path('delete',views.delete),
    #url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], views.protected_serve, {'document_root': settings.MEDIA_ROOT})
    path('%s<path:path>/<path:name>' % settings.MEDIA_URL[1:], views.protected_serve, {'document_root': settings.MEDIA_ROOT})
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)