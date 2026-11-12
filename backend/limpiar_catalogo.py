import re
import pandas as pd

DICCIONARIO_MATERIALES = {
    'PVGR': ('Polivinil', 'Gris'),
    'PVNN': ('Polivinil', 'Negro'),
    'PVNA': ('Polivinil', 'Naranja'),
    'PVNE': ('Polivinil', 'Negro'),
    'PV': ('Polivinil', 'Verde'),
    'PP': ('Polipropileno', None),
    'TPR': ('Caucho Termoplastico', None),
    'CA': ('Caucho', None),
    'PPNE': ('Polipropileno', 'Negro'),
    'N': ('Nylon', None),
    'NYLON': ('Nylon', 'Blanca'),
    'PU': ('Poliuretano', None),
    'NY': ('Nylon', None),
    'AF': ('Goma', None),
    'PB': ('Poliuretano Blando', None),
    'BF': ('Caucho Vulcanizado', None),
    'RHC': ('Caucho/Poliamida', None),
    'PFHT': ('Poliamida/Fibra de Vidrio', None),
    'HPU': ('Poliuretano Termoplastico de Alta Performance', None),
    'HUP': ('Poliuretano Termoendurecido/Hierro', None),
    'PD': ('Poliuretano', None),
    'ALPU': ('Poliuretano/Aluminio', None),
    'AB': ('Caucho/Poliuretano', None),
    'PR': ('Poliamida', None),
    'CPT': ('Caucho Termo-Propulsado', None),
    'ANTIP': ('Poliuretano Blando', None),
    'ALTA TEMP': ('Alta Temperatura (Fenólica)', 'Marron'),
}

MAPA_CATEGORIAS = {
    'EQUIPOS_CARGA': ['CARRETA', 'CARRETILLA', 'PORTACANASTA', 'PORTACILINDRO'],
    'NEUMATICOS': ['NEUMATICO', 'CORAZA', 'LLANTA'],
    'RUEDAS_PARTES': ['RUEDA', 'RDA', 'BALINERA', 'CHUMACERA', 'BUJE', 'RIN', 'SOPORTE', 'TENEDOR'],
    'FERRETERIA': ['BISAGRA', 'ESCUADRA', 'CORREDERA', 'GUIA', 'PATA', 'NIVELADOR'],
    'OTRO': ['DUCHA', 'ACCESORIO']
}


def determinar_categoria(texto):
    if texto.startswith("ROD") or "RODACHINA" in texto:
        return 'Rodachinas'

    for cat, palabras in MAPA_CATEGORIAS.items():
        for p in palabras:
            if re.search(rf'\b{p}\b', texto):
                if cat == 'EQUIPOS_CARGA': return "Equipos de Carga"
                if cat == 'NEUMATICOS':    return "Llantas y Neumáticos"
                if cat == 'RUEDAS_PARTES': return "Ruedas y Partes"
                if cat == 'FERRETERIA':    return "Ferretería y Niveladores"
                if cat == 'OTRO':          return "Accesorios y Otros"
    return "General"


def procesar_producto(nombre_crudo):
    if not isinstance(nombre_crudo, str) or pd.isna(nombre_crudo):
        return {}

    texto = nombre_crudo.upper().strip()
    categoria = determinar_categoria(texto)

    # Inicialización de variables para evitar UnboundLocalError
    diametro = None
    material = None
    color = None
    tipo_fijacion = None
    tiene_freno = False
    especificacion_extra = []

    if categoria == 'Rodachinas':
        # Corregido: 'FRENO' en mayúsculas
        tiene_freno = 'FRENO' in texto

        diametro_match = re.search(r'ROD\s+(\d+(?:\s+\d+/\d+|\s*/\s*\d+)?)', texto)
        if diametro_match:
            diametro = diametro_match.group(1).strip() + '"'

        material = "No especificado"

        # Corregido: 'NYLON' en mayúsculas
        if 'ALTA TEMP' in texto:
            material, color = DICCIONARIO_MATERIALES['ALTA TEMP']
        elif "NYLON" in texto:
            material, color = DICCIONARIO_MATERIALES['NYLON']
        else:
            for codigo, (mat, col) in DICCIONARIO_MATERIALES.items():
                if codigo in texto:
                    material = mat
                    color = col
                    break

        colores_texto = ['NEGRA', 'NEGRO', 'VERDE', 'GRIS', 'NARANJA', 'NAR', 'MARRON', 'BLANCO', 'BLANCA', 'AZUL']
        for c in colores_texto:
            if re.search(rf'\b{c}\b', texto):
                color = 'Naranja' if c == 'NAR' else c.capitalize()
                break

        movimiento = "Fija" if 'FIJA' in texto else 'Giratoria'
        tipo_fijacion = "Platina"

        if re.search(r'\bE\b', texto) or 'ESPIGO' in texto:
            tipo_fijacion = "Espigo"
        elif "PLATAFORMA" in texto or re.search(r'\bP\b', texto):
            tipo_fijacion = "Platina"

        tipo_fijacion = f"{movimiento} - {tipo_fijacion}"

        if "INOX" in texto or "INOXIDABLE" in texto:
            especificacion_extra.append("Herraje Inoxidable")

        partes_nombre = [
            "Rodachina",
            diametro or "",
            material or "",
            f"({color})" if color else "",
            tipo_fijacion or "",
            "con Freno" if tiene_freno else ""
        ]
        nombre_comercial = " ".join([p for p in partes_nombre if p]).strip()
        descripcion = f"Rodachina industrial de {diametro or 'medida estándar'} en {material or 'material resistente'}. Configuración {tipo_fijacion}."

    else:
        medida_match = re.search(r'(\d+(?:\s+\d+/\d+|\s*/\s*\d+)?\s*(?:"|PULG)?)', texto)
        if medida_match:
            diametro = medida_match.group(1).strip()

        nombre_comercial = texto.title()
        descripcion = f"Producto de la categoría {categoria}: {nombre_comercial}. Ideal para aplicaciones de transporte, ensamble y mantenimiento."

    # AHORA EL RETURN ESTÁ FUERA DEL ELSE (sirve para todos)
    return {
        'categoria': categoria,
        'nombre_comercial': re.sub(' +', ' ', nombre_comercial),
        'descripcion': descripcion,
        'diametro': diametro,
        'material': material,
        'color': color,
        'tipo_fijacion': tipo_fijacion,
        'tiene_freno': tiene_freno,
        'especificacion_extra': ", ".join(especificacion_extra) if especificacion_extra else None,
        'es_activa': True
    }


def main():
    archivo_entrada = "inventario.xlsx"
    archivo_salida = "inventario_categorizado.xlsx"

    print('Cargando catálogo completo...')
    df = pd.read_excel(archivo_entrada)
    df = df.rename(columns={'nombre ': 'nombre', 'Categoria': 'categoria'})

    print('Clasificando productos por categoría y procesando atributos...')
    for idx, row in df.iterrows():
        res = procesar_producto(row.get('nombre')) or {}
        df.at[idx, 'categoria'] = res.get('categoria')
        df.at[idx, 'nombre_comercial'] = res.get('nombre_comercial')
        df.at[idx, 'descripcion'] = res.get('descripcion')
        df.at[idx, 'diametro'] = res.get('diametro')
        df.at[idx, 'material'] = res.get('material')
        df.at[idx, 'color'] = res.get('color')
        # Corregido: se lee 'tipo_fijacion'
        df.at[idx, 'tipo_fijacion'] = res.get('tipo_fijacion')
        df.at[idx, 'tiene_freno'] = res.get('tiene_freno')
        df.at[idx, 'especificacion_extra'] = res.get('especificacion_extra')
        df.at[idx, 'es_activa'] = res.get('es_activa')

    df.to_excel(archivo_salida, index=False)
    print(f"\n¡Éxito! Catálogo completo categorizado y procesado en: {archivo_salida}")


if __name__ == '__main__':
    main()
