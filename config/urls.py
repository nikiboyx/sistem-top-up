from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.shortcuts import render

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('shop.urls')),
]

def custom_404_view(request, exception):
    return render(request, 'system_pages/404.html', status=404)

handler404 = custom_404_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
