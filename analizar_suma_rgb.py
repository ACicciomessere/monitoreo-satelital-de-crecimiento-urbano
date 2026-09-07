import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def main():
    directorio_entrada = "descargas_roi"
    dir_mapas = "ciudad_rgb_intervalo"
    os.makedirs(dir_mapas, exist_ok=True)
    
    anios = []
    areas_ciudad_km2 = []
    mask_acumulada = None 

    # --- AJUSTE DE INTERVALO PARA 3 BANDAS (RGB) ---
    # Valores más bajos atrapan el agua, valores más altos atrapan la arena.
    limite_inferior = 0.5  # Sube esto si atrapa mucha agua (ej. 0.6)
    limite_superior = 0.7  # Baja esto si atrapa mucha arena (ej. 0.8)

    print(f"[+] Analizando con suma RGB (Intervalo: {limite_inferior} a {limite_superior})...")

    for year in range(2000, 2027):
        archivo = os.path.join(directorio_entrada, f"imagen_{year}.tif")
        
        if not os.path.exists(archivo):
            continue

        try:
            with rasterio.open(archivo) as src:
                r = src.read(1) 
                g = src.read(2)
                b = src.read(3)
            
            # Sumamos las tres bandas nuevamente
            suma_rgb = r + g + b
            
            # MÁSCARA POR INTERVALO
            mask_actual = (suma_rgb > limite_inferior) & (suma_rgb < limite_superior) & ~np.isnan(suma_rgb)
            
            # Lógica acumulativa: conservamos el crecimiento histórico
            if mask_acumulada is None:
                mask_acumulada = mask_actual
            else:
                mask_acumulada = np.logical_or(mask_acumulada, mask_actual)
            
            # Cálculo de área en km²
            pixeles_ciudad = np.sum(mask_acumulada)
            pixel_area_m2 = 150 * 150
            area_km2 = (pixeles_ciudad * pixel_area_m2) / 1_000_000
            
            anios.append(year)
            areas_ciudad_km2.append(area_km2)
            
            # Generación del mapa visual superpuesto
            rgb = np.dstack((r, g, b))
            rgb_vis = np.clip(rgb, 0, 0.3) / 0.3
            
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.imshow(rgb_vis)
            
            overlay = np.where(mask_acumulada, 1, np.nan)
            ax.imshow(overlay, cmap="autumn", alpha=0.5)
            
            ax.set_title(f"Crecimiento Urbano RGB ({limite_inferior} a {limite_superior}) - {year}\nÁrea Total: {area_km2:.2f} km²", fontsize=16)
            ax.axis("off")
            
            ruta_foto = os.path.join(dir_mapas, f"mapa_{year}.png")
            plt.savefig(ruta_foto, bbox_inches='tight', dpi=150)
            plt.close()
            
            print(f"Año {year} -> Área Acumulada: {area_km2:.2f} km²")
                
        except Exception as e:
            print(f"[x] Error procesando el archivo {archivo}: {e}")

    # Gráfico de línea final
    if anios:
        plt.figure(figsize=(10, 5))
        plt.plot(anios, areas_ciudad_km2, marker='s', color='orange', linestyle='-', linewidth=2)
        plt.title('Expansión Urbana Acumulada (Suma RGB Intervalo)')
        plt.xlabel('Año')
        plt.ylabel('Área de Ciudad (km²)')
        plt.grid(True)
        plt.xticks(anios, rotation=45)
        plt.tight_layout()
        plt.savefig("grafico_crecimiento_rgb_intervalo.png")
        print(f"\n[+] Análisis completado exitosamente.")
        print(f"    - Mapas anuales en: {dir_mapas}/")

if __name__ == "__main__":
    main()
