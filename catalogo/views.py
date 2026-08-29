# Importación de librerías del sistema
import os
import urllib.parse
from pathlib import Path

# Importación de la configuración general de Django
from django.conf import settings

# Herramientas para renderizar plantillas HTML y devolver errores 404
from django.shortcuts import render, get_object_or_404

# Objeto Q: Permite realizar búsquedas avanzadas en la base de datos
from django.db.models import Q

# Clases para construir respuestas HTTP personalizadas
from django.http import HttpResponse

# Permite transformar un archivo HTML y sus variables en una cadena de texto plana
from django.template.loader import render_to_string

# Herramientas de paginación para dividir listas de productos
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# IMPORTACIÓN DE WEASYPRINT: Con soporte para default_url_fetcher
from weasyprint import HTML, CSS, default_url_fetcher

# Importación de las tablas/modelos
from .models import Producto, Categoria, ConfiguracionEmpresa


# FUNCIÓN AUXILIAR: Captura rutas de imágenes y archivos estáticos directamente del disco
def custom_url_fetcher(url, timeout=10, ssl_context=None):
    parsed_url = urllib.parse.urlparse(url)
    url_path = parsed_url.path

    # 1. Intercepta imágenes de la carpeta MEDIA (/media/...)
    if settings.MEDIA_URL and url_path.startswith(settings.MEDIA_URL):
        relative_path = urllib.parse.unquote(url_path[len(settings.MEDIA_URL):])
        file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        
        if os.path.exists(file_path):
            return default_url_fetcher(Path(file_path).as_uri(), timeout, ssl_context)
        else:
            # PREVENCIÓN DE DEADLOCK: Si el archivo no existe en el disco, NO realizar 
            # la petición HTTP interna a 127.0.0.1 (evita congelar runserver).
            return {'string': b'', 'mime_type': 'image/png'}

    # 2. Intercepta archivos ESTÁTICOS (/static/...)
    if settings.STATIC_URL and url_path.startswith(settings.STATIC_URL):
        relative_path = urllib.parse.unquote(url_path[len(settings.STATIC_URL):])
        
        # Modo Producción (STATIC_ROOT)
        if getattr(settings, 'STATIC_ROOT', None):
            file_path = os.path.join(settings.STATIC_ROOT, relative_path)
            if os.path.exists(file_path):
                return default_url_fetcher(Path(file_path).as_uri(), timeout, ssl_context)
                
        # Modo Desarrollo (STATICFILES_DIRS)
        for static_dir in getattr(settings, 'STATICFILES_DIRS', []):
            file_path = os.path.join(static_dir, relative_path)
            if os.path.exists(file_path):
                return default_url_fetcher(Path(file_path).as_uri(), timeout, ssl_context)

        # Si el estático no se encuentra localmente, retorna vacío en vez de bloquear el servidor
        return {'string': b'', 'mime_type': 'text/css'}

    # Si es una URL externa (http/https fuera del dominio local), usa el comportamiento estándar
    return default_url_fetcher(url, timeout, ssl_context)


# VISTA 1: Catálogo Principal (Búsqueda, Filtro, Ordenamiento y Paginación)
def lista_productos(request):
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')
    orden = request.GET.get('orden', '')
    
    productos_list = Producto.objects.filter(disponible=True).select_related('categoria')

    if categoria_id:
        productos_list = productos_list.filter(categoria_id=categoria_id)

    if query:
        productos_list = productos_list.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    if orden == 'precio_asc':
        productos_list = productos_list.order_by('precio')
    elif orden == 'precio_desc':
        productos_list = productos_list.order_by('-precio')
    elif orden == 'nombre_asc':
        productos_list = productos_list.order_by('nombre')
    elif orden == 'nombre_desc':
        productos_list = productos_list.order_by('-nombre')
    else:
        productos_list = productos_list.order_by('-id')

    paginator = Paginator(productos_list, 12) 
    page = request.GET.get('page')

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    categorias = Categoria.objects.all()
    empresa = ConfiguracionEmpresa.objects.first()
    
    return render(request, 'catalogo/lista.html', {
        'productos': productos,
        'categorias': categorias,
        'query': query or '',
        'categoria_id': categoria_id or '',
        'orden': orden,
        'empresa': empresa,
    })


# VISTA 2: Detalle Completo de un Producto
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto.objects.select_related('categoria'), pk=pk, disponible=True)
    empresa = ConfiguracionEmpresa.objects.first()
    
    return render(request, 'catalogo/detalle.html', {
        'producto': producto,
        'empresa': empresa,
    })


# VISTA 3: Generación de PDF utilizando WEASYPRINT
def exportar_pdf(request):
    categoria_id = request.GET.get('categoria', 'todas')
    con_precio = request.GET.get('con_precio') == '1'

    # ORDENAMIENTO OBLIGATORIO: Se ordena por categoría para que {% regroup %} en HTML funcione correctamente.
    # select_related optimiza la consulta BD eliminando llamadas N+1.
    productos = Producto.objects.filter(disponible=True).select_related('categoria').order_by('categoria__nombre', 'nombre')
    categoria_nombre = "Todas las categorías"

    if categoria_id and categoria_id != 'todas':
        try:
            cat = Categoria.objects.get(id=categoria_id)
            productos = productos.filter(categoria=cat)
            categoria_nombre = cat.nombre
        except Categoria.DoesNotExist:
            pass

    empresa = ConfiguracionEmpresa.objects.first()

    # Renderiza la plantilla HTML
    html_string = render_to_string('catalogo/pdf_template.html', {
        'productos': productos,
        'categoria_nombre': categoria_nombre,
        'con_precio': con_precio,
        'empresa': empresa,
    })

    # Generación ultra rápida usando custom_url_fetcher para leer archivos locales
    pdf_bytes = HTML(
        string=html_string, 
        base_url=request.build_absolute_uri('/'),
        url_fetcher=custom_url_fetcher
    ).write_pdf()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="catalogo_{categoria_id}.pdf"'
    
    return response