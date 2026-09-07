import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def main():
    dir_luces = "descargas_luces"
    dir_rgb = "descargas_roi"
    dir_mapas = "ciudad_luces_ajustado"
    os.makedirs(dir_mapas, exist_ok=True)
    
    anios = []
    areas_ciudad_km2 = []
    mask_acumulada = None 

    # --- UMBRALES INDEPENDIENTES POR SATÉLITE ---
    umbral_dmsp = 35   # Para años 2000-2013 (escala 0-63). Sube esto si atrapa arena.
    umbral_viirs = 10 # Para años 2014-2026 (radiancia). Sube a 3.0 o 4.0 si sigue invadiendo.

    print("[+] Analizando expansión urbana con Luces Nocturnas (Umbrales Ajustados)...")

    for year in range(2000, 2027):
        arch_luz = os.path.join(dir_luces, f"luces_{year}.tif")
        arch_rgb = os.path.join(dir_rgb, f"imagen_{year}.tif")
        
        if not os.path.exists(arch_luz) or not os.path.exists(arch_rgb):
            continue

        try:
            with rasterio.open(arch_luz) as src:
                luz_np = src.read(1)
            
            # Aplicamos el umbral correcto dependiendo del año y el satélite
            if year <= 2013:
                mask_actual = (luz_np > umbral_dmsp) & ~np.isnan(luz_np)
                sensor_usado = f"DMSP (> {umbral_dmsp})"
            else:
                mask_actual = (luz_np > umbral_viirs) & ~np.isnan(luz_np)
                sensor_usado = f"VIIRS (> {umbral_viirs})"
            
            # Lógica acumulativa
            if mask_acumulada is None:
                mask_acumulada = mask_actual
            else:
                mask_acumulada = np.logical_or(mask_acumulada, mask_actual)
            
            # Cálculo de área (píxeles de 150x150m)
            pixeles_ciudad = np.sum(mask_acumulada)
            area_km2 = (pixeles_ciudad * 150 * 150) / 1_000_000
            
            anios.append(year)
            areas_ciudad_km2.append(area_km2)
            
            # Generar mapa con fondo RGB para verificar visualmente
            with rasterio.open(arch_rgb) as src_rgb:
                r = src_rgb.read(1)
                g = src_rgb.read(2)
                b = src_rgb.read(3)
                
            rgb = np.dstack((r, g, b))
            rgb_vis = np.clip(rgb, 0, 0.3) / 0.3
            
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.imshow(rgb_vis)
            
            overlay = np.where(mask_acumulada, 1, np.nan)
            ax.imshow(overlay, cmap="autumn", alpha=0.5)
            
            ax.set_title(f"Ciudad Iluminada Acumulada - {year}\nSensor: {sensor_usado} | Área: {area_km2:.2f} km²", fontsize=16)
            ax.axis("off")
            
            plt.savefig(os.path.join(dir_mapas, f"mapa_luces_{year}.png"), bbox_inches='tight', dpi=150)
            plt.close()
            
            print(f"Año {year} -> Sensor: {sensor_usado[:5]} | Área Acumulada: {area_km2:.2f} km²")
                
        except Exception as e:
            print(f"[x] Error procesando el archivo {arch_luz}: {e}")

    # Generamos el gráfico final
    if anios:
        plt.figure(figsize=(10, 5))
        plt.plot(anios, areas_ciudad_km2, marker='o', color='gold', markeredgecolor='black', linestyle='-', linewidth=2)
        plt.title('Expansión Urbana Acumulada (Luces Nocturnas)')
        plt.xlabel('Año')
        plt.ylabel('Área de Ciudad (km²)')
        plt.grid(True)
        plt.xticks(anios, rotation=45)
        plt.tight_layout()
        plt.savefig("grafico_crecimiento_luces_ajustado.png")
        print(f"\n[+] Análisis completado. Resultados en carpeta '{dir_mapas}'.")

if __name__ == "__main__":
    main()
