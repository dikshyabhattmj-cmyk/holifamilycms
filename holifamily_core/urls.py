from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, FileResponse
import os

def service_worker_view(request):
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    if os.path.exists(sw_path):
        with open(sw_path, 'rb') as f:
            content = f.read()
        response = HttpResponse(content, content_type='application/javascript')
        response['Service-Worker-Allowed'] = '/'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    return HttpResponse("// sw not found", content_type='application/javascript', status=404)

urlpatterns = [
    path('sw.js', service_worker_view, name='service_worker'),
    path('admin/', admin.site.urls),
    path('portal/', include('portal.urls')),
    path('', include('school.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

admin.site.site_header = "Holi Family Secondary School - Administration"
admin.site.site_title = "Holi Family Portal"
admin.site.index_title = "School System Management"

