from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Importamos la nueva vista exportar_pdf
from catalogo.views import lista_productos, detalle_producto, exportar_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lista_productos, name='lista_productos'),
    path('producto/<int:pk>/', detalle_producto, name='detalle_producto'),
    path('exportar-pdf/', exportar_pdf, name='exportar_pdf'),  # <--- Ruta agregada
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)