from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from talent_score.yasg import urlpatterns as doc_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('user/', include('users.urls')), 
    path("__debug__/", include("debug_toolbar.urls")),
    # Uploaded files (profile photos, reports, CVs) from the persistent volume.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += doc_urls