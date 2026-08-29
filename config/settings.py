"""
Configuración global del proyecto 'config' en Django.
"""

import os
from pathlib import Path

# 1. RUTA BASE Y SEGURIDAD

# Calcula la ruta absoluta de la carpeta raíz de tu proyecto en la computadora
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta única utilizada por Django para la firma criptográfica y tokens de seguridad
SECRET_KEY = 'django-insecure-heqw-2k%%^+!r203@0266c=zat35-sv-+nu!d^l3*6f4iwyqle'

# Modo depuración ( True = Muestra errores detallados en pantalla mientras desarrollas )
# ¡IMPORTANTE!: Debe cambiarse a 'False' cuando la página esté pública en un servidor real
DEBUG = True

# Dominio o IPs desde donde se permite acceder a la web (ej. ['mientorno.com', 'localhost'])
ALLOWED_HOSTS = []

# 2. APLICACIONES E INTERMEDIARIOS (PLUGINS Y MÓDULOS)

# Lista de todos los módulos activos en el proyecto.
INSTALLED_APPS = [
    'jazzmin',  # Tema visual moderno para personalizar el panel administrativo (va antes del admin)
    'django.contrib.admin',        # Panel de administración predeterminado
    'django.contrib.auth',         # Sistema de usuarios y contraseñas
    'django.contrib.contenttypes', # Manejo de tipos de contenido e infraestructura interna
    'django.contrib.sessions',     # Manejo de sesiones de usuario (mantener sesión iniciada)
    'django.contrib.messages',     # Sistema de alertas y mensajes temporales
    'django.contrib.staticfiles',  # Manejo de archivos CSS, JavaScript e imágenes de plantilla
    
    # Tu propia aplicación instalada
    'catalogo',
]

# Capas de seguridad y procesamiento intermedias por las que pasa cada petición web
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',             # Protege contra ataques de formularios falsos
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Asocia usuarios con sesiones activas
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protege contra incrustaciones no autorizadas en iframes
]

# Archivo de rutas principales que iniciará la navegación del sitio
ROOT_URLCONF = 'config.urls'

# Motor de plantillas HTML y procesadores de contexto globales
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # Carpetas adicionales de HTML fuera de las apps
        'APP_DIRS': True, # Le indica a Django que busque plantillas dentro de cada app (ej: catalogo/templates)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Conexión para el servidor web (WSGI)
WSGI_APPLICATION = 'config.wsgi.application'

# 3. BASE DE DATOS

# Configuración del motor de la base de datos (por defecto SQLite3)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # Genera el archivo db.sqlite3 en la raíz del proyecto
    }
}

# 4. REGLAS DE CONTRASEÑAS

# Validadores automáticos para evitar que los usuarios creen contraseñas muy débiles o cortas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 5. IDIOMA Y HORARIO

# Código de idioma de la interfaz (Español)
LANGUAGE_CODE = 'es-pe'

# Zona horaria del proyecto (Sincronizado con la hora local)
TIME_ZONE = 'America/Lima'

# Habilita el sistema de internacionalización y traducción de Django
USE_I18N = True

# Habilita el soporte para zonas horarias
USE_TZ = True

# 6. ARCHIVOS ESTÁTICOS Y MULTIMEDIA

# Ruta URL pública para archivos estáticos del sistema (CSS, JS)
STATIC_URL = 'static/'

# Ruta URL pública para acceder a las fotos subidas por los usuarios
MEDIA_URL = '/media/'

# Ruta física en el disco duro donde se guardarán las fotos subidas desde el Admin (ej: la foto del producto o logo)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 7. PERSONALIZACIÓN DEL TEMA JAZZMIN (ADMIN)

# Opciones de diseño para la plantilla de administración
JAZZMIN_SETTINGS = {
    "site_title": "Catálogo Admin",       # Título en la pestaña del navegador
    "site_header": "Catálogo Digital",     # Título en la barra superior del Admin
    "site_brand": "MegaBit",           # Marca o nombre en el menú lateral
    "welcome_sign": "Bienvenido al Panel de Administración", # Mensaje del Login
    "topmenu_links": [
        {"name": "Ver Sitio Web",  "url": "/", "permissions": ["auth.view_user"]}, # Enlace directo a la tienda
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
}