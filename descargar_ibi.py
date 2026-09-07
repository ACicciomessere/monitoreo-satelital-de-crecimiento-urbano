import ee
import geemap
import os

def main():
    print("Iniciando autenticación...")
    ee.Authenticate() #[cite: 1]
    ee.Initialize(project='imposing-carver-505921-e0') #[cite: 1]

    coordenadas = [
        [54.835508581355924, 25.774898334769915],
        [55.823473728975500, 25.774898334769915],
        [55.823473728975500, 24.835080741810813],
        [54.835508581355924, 24.835080741810813],
        [54.835508581355924, 25.774898334769915]
    ]
    roi = ee.Geometry.Polygon([coordenadas]) #[cite: 3]

    directorio_salida = "descargas_ibi"
    os.makedirs(directorio_salida, exist_ok=True) #[cite: 3]

    for year in range(2000, 2027):
        fecha_inicio = f'{year}-01-01'
        fecha_fin = f'{year}-12-31'
        
        try:
            if year <= 2012:
                # Landsat 7
                coleccion = ee.ImageCollection("LANDSAT/LE07/C02/T1_TOA")
                g, r, nir, swir1 = 'B2', 'B3', 'B4', 'B5'
            else:
                # Landsat 8
                coleccion = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA")
                g, r, nir, swir1 = 'B3', 'B4', 'B5', 'B6'

            # Mosaico anual mediano recortado
            mosaico = coleccion.filterBounds(roi) \
                               .filterDate(fecha_inicio, fecha_fin) \
                               .median() \
                               .clip(roi)
            
            # 1. Calculamos NDBI (Ciudad)
            ndbi = mosaico.normalizedDifference([swir1, nir]).rename('NDBI') #[cite: 1]
            
            # 2. Calculamos MNDWI (Agua)
            mndwi = mosaico.normalizedDifference([g, swir1]).rename('MNDWI') #[cite: 1]
            
            # 3. Calculamos SAVI (Suelo/Vegetación)
            savi = mosaico.expression(
                '((NIR - RED) / (NIR + RED + 0.5)) * 1.5', {
                    'NIR': mosaico.select(nir),
                    'RED': mosaico.select(r)
                }).rename('SAVI')

            # 4. Ecuación Maestra IBI
            ibi = mosaico.expression(
                '(NDBI - (SAVI + MNDWI) / 2.0) / (NDBI + (SAVI + MNDWI) / 2.0)', {
                    'NDBI': ndbi,
                    'SAVI': savi,
                    'MNDWI': mndwi
                }).rename('IBI')

            archivo_salida = os.path.join(directorio_salida, f"ibi_{year}.tif")
            print(f"[+] Exportando índice IBI del año {year}...")
            
            geemap.ee_export_image(ibi, filename=archivo_salida, scale=150, region=roi, file_per_band=False)
        except Exception as e:
            print(f"[x] Error al procesar el año {year}: {e}")

if __name__ == "__main__":
    main()
