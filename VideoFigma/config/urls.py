from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('custom_auth/', include('videos.custom_auth.api_urls')),
        path('registration/', include('videos.registrations.api_urls')),
        path('post/', include('videos.post.api_urls')),
    ])),

    path('web/', include([
        path('custom_auth/', include('videos.custom_auth.web_urls')),
        # path('registration/', include('videos.registrations.web_urls')),
        # path('post/', include('videos.post.web_urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
