import rasterio
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def main():
    # Verificamos que se haya pasado el argumento al ejecutar el script
    if len(sys.argv) < 2:
        print("Uso correcto: python3 ver_tiff.py <ruta_al_archivo.tif>")
        sys.exit(1)
        
    # Capturamos el archivo pasado por la terminal
    archivo = sys.argv[1]

    # Validamos que el archivo realmente exista antes de intentar abrirlo
    if not os.path.exists(archivo):
        print(f"[-] Error: El archivo '{archivo}' no existe.")
        sys.exit(1)

    print(f"[+] Abriendo {archivo} ...")

    try:
        # Abrimos el archivo ráster y extraemos sus datos y metadatos[cite: 2]
        with rasterio.open(archivo) as src:
            bandas = src.count #[cite: 2]
            
            if bandas >= 3:
                # Si tiene 3 o más bandas, lo tratamos como una imagen RGB
                r = src.read(1)
                g = src.read(2)
                b = src.read(3)
                img = np.dstack((r, g, b))
                
                # Normalizamos (stretch) para que los colores se vean bien[cite: 1, 2]
                img = np.clip(img, 0, 0.3) / 0.3
                titulo = "Visualización RGB"
            else:
                # Si es de 1 banda (como las de Luces, NDBI o Rojo)
                img = src.read(1)
                titulo = "Visualización de Una Banda"

        # Graficamos la imagen[cite: 1]
        plt.figure(figsize=(10, 10))
        if bandas >= 3:
            plt.imshow(img) #[cite: 1]
        else:
            plt.imshow(img, cmap='gray') 
            plt.colorbar(label='Valor del píxel') #[cite: 2]

        plt.title(f"{titulo}\n{os.path.basename(archivo)}", fontsize=14)
        plt.axis("off") #[cite: 1]
        plt.tight_layout() #[cite: 1]
        plt.show() #[cite: 1]
        
    except Exception as e:
        print(f"[x] Error al abrir la imagen: {e}")

if __name__ == "__main__":
    main()
