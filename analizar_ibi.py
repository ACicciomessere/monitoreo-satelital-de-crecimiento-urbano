import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def main():
    dir_ibi = "descargas_ibi"
    dir_rgb = "descargas_roi" 
    dir_mapas = "ciudad_ibi"
    os.makedirs(dir_mapas, exist_ok=True)
    
    anios = []
    areas_ciudad_km2 = []
    mask_acumulada = None 

    print("[+] Analizando crecimiento urbano con índice IBI (Intervalo Manual y Debug)...")

    for year in range(2000, 2027):
        arch_ibi = os.path.join(dir_ibi, f"ibi_{year}.tif")
        arch_rgb = os.path.join(dir_rgb, f"imagen_{year}.tif")
        
        if not os.path.exists(arch_ibi) or not os.path.exists(arch_rgb):
            continue

        try:
            with rasterio.open(arch_ibi) as src:
                ibi_np = src.read(1)
                
            # --- DEBUG: Imprimimos el rango real del IBI ---
            min_val = np.nanmin(ibi_np)
            max_val = np.nanmax(ibi_np)
            print(f"--> Año {year} | Rango IBI real: Mínimo {min_val:.3f} | Máximo {max_val:.3f}")
            
            # --- AJUSTE DE INTERVALO IBI ---
            umbral_inferior = -2  # Bajamos el piso a valores negativos
            umbral_superior = 1.5    # Mantenemos el techo alto
            
            # Filtramos aplicando ambos umbrales y descartando nulos
            mask_actual = (ibi_np > umbral_inferior) & (ibi_np < umbral_superior) & ~np.isnan(ibi_np)
            
            # Lógica acumulativa: la ciudad construida no se borra
            if mask_acumulada is None:
                mask_acumulada = mask_actual
            else:
                mask_acumulada = np.logical_or(mask_acumulada, mask_actual)
            
            # Cálculo de área
            pixeles_ciudad = np.sum(mask_acumulada)
            area_km2 = (pixeles_ciudad * 150 * 150) / 1_000_000
            
            anios.append(year)
            areas_ciudad_km2.append(area_km2)
            
            # Generar mapa con fondo RGB
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
            
            ax.set_title(f"Crecimiento Urbano IBI ({umbral_inferior} a {umbral_superior}) - {year}\nÁrea Total: {area_km2:.2f} km²", fontsize=16)
            ax.axis("off")
            
            plt.savefig(os.path.join(dir_mapas, f"mapa_ibi_{year}.png"), bbox_inches='tight', dpi=150)
            plt.close()
            
            print(f"    Resultado {year}: Área Acumulada = {area_km2:.2f} km²\n")
                
        except Exception as e:
            print(f"[x] Error procesando el archivo {arch_ibi}: {e}")

    # Generamos el gráfico
    if anios:
        plt.figure(figsize=(10, 5))
        plt.plot(anios, areas_ciudad_km2, marker='o', color='darkred', linestyle='-', linewidth=2)
        plt.title('Expansión Urbana Acumulada (Índice IBI con Techo)')
        plt.xlabel('Año')
        plt.ylabel('Área de Ciudad (km²)')
        plt.grid(True)
        plt.xticks(anios, rotation=45)
        plt.tight_layout()
        plt.savefig("grafico_crecimiento_ibi_ajustado.png")
        print(f"\n[+] Análisis completado. Resultados en carpeta '{dir_mapas}'.")

if __name__ == "__main__":
    main()
