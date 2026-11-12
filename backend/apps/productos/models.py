from django.db import models

# Create your models here.

class Producto(models.Model):

    codigo = models.CharField(max_length=100, unique=True, verbose_name="ID / Referencia")
    nombre_original = models.CharField(max_length=255, verbose_name="Nombre original")
    nombre = models.CharField(max_length=255, verbose_name="Nombre comercial")
    categoria = models.CharField(max_length=100, verbose_name="Categoria")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripcion")

    costo = models.DecimalField(max_digits=12, decimal_places=2, default=0.0 , verbose_name="Costo")
    cantidad = models.IntegerField(default=0, verbose_name="Cantidad")

    diametro = models.CharField(max_length=50, blank=True, null=True,   verbose_name="Diámetro")
    material = models.CharField(max_length=100, blank=True, null=True, verbose_name="Material")
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color")
    tiene_freno = models.BooleanField(default=False, null=True, verbose_name="¿Tiene freno?")
    tipo_fijacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo fijacion")
    especificacion_extra = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especificacion extra")

    capacidad = models.IntegerField(default=0, verbose_name="Capacidad")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen")

    es_activa= models.BooleanField(default=False, verbose_name="Es activa")
    creada = models.DateField(auto_now_add=True, verbose_name="Creada")
    actualizada = models.DateField(auto_now=True, verbose_name="Actualiza")

    def __str__(self):
        return f"{self.id} | {self.nombre}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["categoria", "nombre"]
