from django.contrib import admin
from .models import Producto
# Register your models here.

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id','codigo','nombre', 'categoria', 'costo', 'cantidad', 'tiene_freno', 'es_activa')
    list_filter = ('categoria', 'tiene_freno', 'es_activa')
    search_fields = ('id', 'nombre', 'nombre_original')