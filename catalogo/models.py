# Importamos el módulo 'models' de Django, que nos permite construir las tablas de la base de datos como clases de Python.
from django.db import models

# 1. TABLA: Categoria

class Categoria(models.Model):
    # Campo de texto corto (máx. 100 caracteres) para el nombre de la categoría (ej. "Laptops")
    nombre = models.CharField(max_length=100)

    # Subclase Meta: Configura cómo se comportará esta tabla en el panel de administración
    class Meta:
        # Corrige el plural en el Admin para que no diga "Categorias" sin tilde
        verbose_name_plural = "Categorías"

    # Método __str__: Define cómo se mostrará este objeto como texto en el Admin o listas desplegables
    def __str__(self):
        return self.nombre

# 2. TABLA: Producto

class Producto(models.Model):
    # Lista de opciones fijas para la etiqueta de estado del producto.
    # El primer elemento del tuple es lo que guarda la BD, el segundo es lo que ve el usuario.
    ESTADO_CHOICES = [
        ('NINGUNO', 'Sin etiqueta'),
        ('NUEVO', 'Nuevo'),
        ('OFERTA', 'En Oferta'),
        ('AGOTADO', 'Agotado'),
    ]
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    # Nombre comercial del producto (hasta 200 caracteres)
    nombre = models.CharField(max_length=200)

    # Texto extenso para un resumen rápido del producto. 'blank=True' hace que no sea obligatorio llenarlo
    descripcion = models.TextField(verbose_name="Descripción Corta", blank=True)

    # Texto extenso para fichas técnicas complejas. 'help_text' muestra un mensaje de ayuda en el Admin
    especificaciones = models.TextField(
        verbose_name="Especificaciones Técnicas", 
        blank=True, 
        help_text="Puedes escribir características detalladas del producto."
    )

    # Campo decimal para el precio exacto (hasta 10 dígitos en total y 2 decimales, ej: 99,999,999.99)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    # Desplegable de etiquetas. Usa las opciones definidas en ESTADO_CHOICES y por defecto asigna 'NINGUNO'
    etiqueta = models.CharField(
        max_length=10, 
        choices=ESTADO_CHOICES, 
        default='NINGUNO', 
        verbose_name="Etiqueta / Estado"
    )

    # Imagen principal. Se sube a la carpeta 'media/productos/'. Puede quedar vacía ('blank=True, null=True')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    # Relación de clave foránea (ForeignKey): Vincula el producto a una Categoria.
    # 'on_delete=models.CASCADE': Si borras la categoría, se eliminan todos sus productos.
    # 'related_name='productos'': Permite buscar desde Categoria todos sus productos (ej: categoria.productos.all())
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    # Interruptor booleano (Sí/No) para ocultar o mostrar el producto sin borrarlo de la base de datos
    disponible = models.BooleanField(default=True)

    # Captura automáticamente la fecha y hora exacta en la que se crea el producto por primera vez
    creado_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre  

# 3. TABLA: ImagenProducto (Galería Adicional)

class ImagenProducto(models.Model):
    # Vincula esta imagen extra a un Producto específico.
    # Permite que un solo producto tenga muchas imágenes asociadas (Relación 1 a Muchos)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')

    # Guarda la ruta de las fotos adicionales en la carpeta 'media/productos/galeria/'
    imagen = models.ImageField(upload_to='productos/galeria/', verbose_name="Imagen")

    class Meta:
        verbose_name = "Imagen adicional"
        verbose_name_plural = "Galería de imágenes"

    def __str__(self):
        # Muestra en el Admin a qué producto pertenece la foto
        return f"Imagen de {self.producto.nombre}"

# 4. TABLA: ConfiguracionEmpresa (Datos Globales)

class ConfiguracionEmpresa(models.Model):
    # Nombre de la empresa que se muestra en el encabezado e informes PDF
    nombre = models.CharField(max_length=100, default="Mi Empresa S.A.C.", verbose_name="Nombre de la empresa")

    # Logo institucional guardado en la carpeta 'media/empresa/'
    logo = models.ImageField(upload_to='empresa/', blank=True, null=True, verbose_name="Logo de la empresa")

    class Meta:
        verbose_name = "Configuración de la Empresa"
        verbose_name_plural = "Configuración de la Empresa"

    def __str__(self):
        return self.nombre