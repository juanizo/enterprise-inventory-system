import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.productos.models import Producto
import pandas as pd

def upload_data_db():

    df = pd.read_excel('inventario_categorizado.xlsx')

    creados=0
    actualizados=0

    for _, row in df.iterrows():

        codigo = str(row.get('id','')).strip()
        if not codigo or codigo == 'nan':
            continue

        costo = row.get('costo',0)
        costo = 0 if pd.isna(costo) else costo

        cantidad = row.get('unidades',0)
        cantidad = 0 if pd.isna(cantidad) else int(cantidad)

        capacidad = row.get('capacidad',0)
        capacidad = 0 if pd.isna(capacidad) else int(capacidad)

        obj, created = Producto.objects.update_or_create(
            codigo=codigo,
            defaults={
                'nombre_original': str(row.get('nombre_original','')),
                'nombre': str(row.get('nombre','')),
                'categoria': str(row.get('categoria','General')),
                'descripcion': str(row.get('descripcion','')),
                'costo':costo,
                'cantidad':cantidad,
                'diametro': row.get('diametro') if not pd.isna(row.get('diametro')) else None,
                'material':row.get('material') if not pd.isna(row.get('material')) else None ,
                'color':row.get('color') if not pd.isna(row.get('color')) else None,
                'tipo_fijacion':row.get('tipo_fijacion') if not pd.isna(row.get('tipo_fijacion')) else None,
                'tiene_freno': bool(row.get('tiene_freno', False)),
                'especificacion_extra': str(row.get('especificaciones_extra')) if not pd.isna(row.get('especificaciones_extra')) else None,
                'es_activa': bool(row.get('es_activa', True)),
                'capacidad': capacidad,

            }

        )

        if created:
            creados += 1
        else:
            actualizados += 1

        print(f'\n !Carga completada con exito')
        print(f'Productos nuevos creados: {creados}')
        print(f'Productos actualizados: {actualizados}')
        print(f'Productos total base de datos: {Producto.objects.count()}' )

if __name__ == '__main__':
    upload_data_db()