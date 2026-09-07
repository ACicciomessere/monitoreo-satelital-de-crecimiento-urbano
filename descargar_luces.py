import ee
import geemap
import os

def main():
    ee.Authenticate()
    ee.Initialize(project='imposing-carver-505921-e0')

    coordenadas = [
        [54.835508581355924, 25.774898334769915], [55.823473728975500, 25.774898334769915],
        [55.823473728975500, 24.835080741810813], [54.835508581355924, 24.835080741810813],
        [54.835508581355924, 25.774898334769915]
    ]
    roi = ee.Geometry.Polygon([coordenadas])

    dir_salida = "descargas_luces"
    os.makedirs(dir_salida, exist_ok=True)

    for year in range(2000, 2027):
        try:
            if year <= 2013:
                # DMSP-OLS (Anual)
                coleccion = ee.ImageCollection("NOAA/DMSP-OLS/NIGHTTIME_LIGHTS")
                luz = coleccion.filterDate(f'{year}-01-01', f'{year}-12-31').first().select('stable_lights')
            else:
                # VIIRS (Mensual, sacamos mediana)
                coleccion = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG")
                luz = coleccion.filterDate(f'{year}-01-01', f'{year}-12-31').median().select('avg_rad')

            arch_salida = os.path.join(dir_salida, f"luces_{year}.tif")
            print(f"[+] Exportando Luces de {year}...")
            geemap.ee_export_image(luz.clip(roi), filename=arch_salida, scale=150, region=roi, file_per_band=False)
        except Exception as e:
            print(f"[x] Error en {year}: {e}")

if __name__ == "__main__":
    main()
