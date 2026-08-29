# Importación del módulo de formularios de Django para modificar componentes visuales (widgets)
from django import forms

# Importación del motor del panel de administración
from django.contrib import admin

# Importación de los modelos de autenticación nativos de Django (Usuarios y Grupos)
from django.contrib.auth.models import User, Group

# Importación del administrador por defecto de usuarios y su formulario de edición
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

# Función para permitir la renderización segura de código HTML personalizado en la interfaz
from django.utils.safestring import mark_safe

# Importación de tus modelos personalizados definidos en models.py
from .models import Categoria, Producto, ImagenProducto, ConfiguracionEmpresa


# 1. PERSONALIZACIÓN DE AUTENTICACIÓN Y USUARIOS

# Oculta la sección predeterminada de 'Grupos' para simplificar la navegación del Admin
admin.site.unregister(Group)

# Widget visual personalizado para ocultar el hash de la contraseña por asteriscos estéticos
class PasswordAsteriscosWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        # Devuelve código HTML que muestra asteriscos y un botón estilizado con Bootstrap para cambiar la clave
        return mark_safe(
            '<div style="display: flex; align-items: center; gap: 12px; padding: 4px 0;">'
            '<span style="font-size: 1.2rem; font-weight: bold; letter-spacing: 4px; color: #212529;">************</span>'
            '<a class="btn btn-sm btn-outline-primary ms-2" href="../password/">'
            '<i class="fas fa-key me-1"></i> Cambiar contraseña'
            '</a>'
            '</div>'
        )

# Formulario personalizado que reemplaza la vista por defecto de edición de usuarios
class MiUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asigna nuestro widget de asteriscos al campo de contraseña
        self.fields['password'].widget = PasswordAsteriscosWidget()
        # Elimina el texto de ayuda predeterminado de Django sobre claves
        self.fields['password'].help_text = ''

# Traducción y simplificación de nombres de campos en la interfaz para usuarios finales
User._meta.get_field('username').verbose_name = 'Nombre de usuario'
User._meta.get_field('is_active').verbose_name = 'Cuenta activa'
User._meta.get_field('is_active').help_text = 'Permite o bloquea el ingreso de este usuario al sistema.'

User._meta.get_field('is_staff').verbose_name = 'Acceso al Panel (Personal)'
User._meta.get_field('is_staff').help_text = 'Permite al usuario ingresar a gestionar el catálogo.'

User._meta.get_field('is_superuser').verbose_name = 'Administrador General'
User._meta.get_field('is_superuser').help_text = 'Otorga control total del sistema y gestión de otros usuarios.'

# Se remueve la configuración por defecto de usuarios para aplicar la personalizada
admin.site.unregister(User)

# Se registra de nuevo la gestión de usuarios con un diseño limpio
@admin.register(User)
class UsuarioSimplificadoAdmin(UserAdmin):
    form = MiUserChangeForm # Aplica el formulario con asteriscos
    list_display = ('username', 'is_staff', 'is_superuser', 'is_active') # Columnas en la tabla general
    list_filter = () # Elimina filtros laterales innecesarios
    actions = ['delete_selected'] # Mantiene la acción de borrado masivo
    search_fields = ('username',) # Buscador por nombre de usuario
    ordering = ('username',) # Ordena alfabéticamente

    # Organización de los bloques de edición de un usuario existente
    fieldsets = (
        ('Datos de Ingreso', {
            'fields': ('username', 'password')
        }),
        ('Nivel de Jerarquía', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )

    # Organización del formulario cuando se crea un usuario desde cero
    add_fieldsets = (
        ('Crear Nuevo Usuario', {
            'classes': ('wide',),
            'fields': ('username', 'password', 'is_staff', 'is_superuser'),
        }),
    )

    filter_horizontal = ()


# 2. GESTIÓN DE CATEGORÍAS

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',) # Muestra el nombre en la lista principal
    search_fields = ('nombre',) # Permite buscar categorías por texto
    actions = ['delete_selected']


# 3. GESTIÓN DE PRODUCTOS Y GALERÍA

# Widget personalizado para mostrar el símbolo de Soles (S/) antes de la casilla
class MonedaSolesWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        return mark_safe(
            f'<div style="display: inline-flex; align-items: center; gap: 6px;">'
            f'<span style="font-weight: bold; color: #1e293b; font-size: 14px;">S/</span>'
            f'{input_html}'
            f'</div>'
        )

# Formulario para la vista de EDICIÓN INDIVIDUAL del producto
class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'precio': MonedaSolesWidget(attrs={
                'style': 'background-color: #ffffff; border: 1px solid #d1d5db; border-radius: 8px; padding: 6px 12px; width: 110px; font-size: 14px; outline: none;',
                'step': '0.01',
            }),
            'stock': forms.NumberInput(attrs={
                'style': 'background-color: #ffffff; border: 1px solid #d1d5db; border-radius: 8px; padding: 6px 12px; width: 100px; font-size: 14px; outline: none;',
            }),
        }

# Formulario para la TABLA PRINCIPAL (list_editable)
class ProductoChangelistForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'precio': MonedaSolesWidget(attrs={
                'style': 'background-color: #ffffff; border: 1px solid #d1d5db; border-radius: 8px; padding: 6px 12px; width: 90px; font-size: 14px; outline: none; box-shadow: none;',
            }),
            'stock': forms.NumberInput(attrs={
                'style': 'background-color: #ffffff; border: 1px solid #d1d5db; border-radius: 8px; padding: 6px 12px; width: 90px; font-size: 14px; outline: none; box-shadow: none;',
            }),
        }

# Edición de galería de imágenes en línea
class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 3

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    form = ProductoAdminForm
    
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'disponible')
    list_editable = ('precio', 'stock', 'disponible')
    list_filter = ()
    search_fields = ('nombre', 'descripcion')
    actions = ['delete_selected']
    inlines = [ImagenProductoInline]

    def get_changelist_form(self, request, **kwargs):
        return ProductoChangelistForm