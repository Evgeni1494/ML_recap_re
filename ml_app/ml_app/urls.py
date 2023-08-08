from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_app.urls')),
    path('', include('evaluation_app.urls')),
    path('', include('monitoring_app.urls')),
]

# Cette partie sert vos fichiers statiques via Django lorsque DEBUG est désactivé
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

