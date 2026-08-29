# Importa la función 'path' de Django, la cual sirve para asociar una URL a una vista específica
from django.urls import path

# Importa el archivo 'views.py' de la misma carpeta actual (catalogo)
from . import views

# Lista principal donde se registran todas las rutas de la aplicación
urlpatterns = [
    # ... tus rutas anteriores (como la página de inicio/lista o el detalle del producto)

    # RUTA: Generación de PDF
    # 1. 'exportar-pdf/': Es la dirección visible en el navegador (ej: tudominio.com/exportar-pdf/)
    # 2. views.exportar_pdf: Es la función dentro de views.py que procesa y devuelve el PDF
    # 3. name='exportar_pdf': Es el apodo interno para invocar la ruta desde las plantillas con {% url 'exportar_pdf' %}
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
]