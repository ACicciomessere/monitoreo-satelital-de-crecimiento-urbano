import sys
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        print("Uso correcto: python3 ver_ibi.py <año>")
        sys.exit(1)
        
    try:
        year = int(sys.argv[1])
    except ValueError:
        print("[-] Error: El año debe ser un número (ej. 2005).")
        sys.exit(1)

    archivo = os.path.join("descargas_ibi", f"ibi_{year}.tif")

    if not os.path.exists(archivo):
        print(f"[-] Error: El archivo '{archivo}' no existe.")
        sys.exit(1)

    print(f"[+] Abriendo datos IBI de {year} ...")

    try:
        with rasterio.open(archivo) as src:
            ibi = src.read(1)

        plt.figure(figsize=(10, 8))
        
        # Recortamos visualmente los valores a tu rango de análisis (-2 a 1.5)
        ibi_vis = np.clip(ibi, -2, 1.5)

        # Usamos el mapa de colores y ajustamos los límites de la gráfica
        im = plt.imshow(ibi_vis, cmap='RdBu_r', vmin=-2.0, vmax=1.5)
        plt.title(f"Índice IBI Dubái - {year}\n(Rango de análisis: -2.0 a 1.5)", fontsize=14)

        plt.colorbar(im, label='Valor IBI (-2.0 Agua/Arena, +1.5 Ciudad)')
        plt.axis("off")
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"[x] Error al abrir la imagen: {e}")

if __name__ == "__main__":
    main()
