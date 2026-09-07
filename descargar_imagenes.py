import ee
import geemap
import os

def main():
    print("Iniciando autenticación...")
    ee.Authenticate()
    ee.Initialize(project='imposing-carver-505921-e0')

    coordenadas = [
        [54.835508581355924, 25.774898334769915],
        [55.823473728975500, 25.774898334769915],
        [55.823473728975500, 24.835080741810813],
        [54.835508581355924, 24.835080741810813],
        [54.835508581355924, 25.774898334769915]
    ]
    roi = ee.Geometry.Polygon([coordenadas])

    directorio_salida = "descargas_roi"
    os.makedirs(directorio_salida, exist_ok=True)

    for year in range(2000, 2027):
        fecha_inicio = f'{year}-01-01'
        fecha_fin = f'{year}-12-31'
        
        try:
            # Usamos Landsat 7 hasta 2012, luego el moderno Landsat 8
            if year <= 2012:
                coleccion = ee.ImageCollection("LANDSAT/LE07/C02/T1_TOA")
                bandas_rgb = ['B3', 'B2', 'B1'] 
            else:
                coleccion = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA")
                bandas_rgb = ['B4', 'B3', 'B2'] 

            # LA CLAVE: Seleccionar bandas, calcular mediana anual y recortar al rectángulo exacto
            mosaico_anual = coleccion.filterBounds(roi) \
                                     .filterDate(fecha_inicio, fecha_fin) \
                                     .select(bandas_rgb) \
                                     .median() \
                                     .clip(roi)
            
            archivo_salida = os.path.join(directorio_salida, f"imagen_{year}.tif")
            
            print(f"[+] Exportando mosaico perfecto del año {year}...")
            
            geemap.ee_export_image(
                mosaico_anual, 
                filename=archivo_salida, 
                scale=150, 
                region=roi,
                file_per_band=False
            )
        except Exception as e:
            print(f"[x] Error al procesar el año {year}: {e}")

if __name__ == "__main__":
    main()
