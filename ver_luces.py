import sys
import os
import rasterio
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        print("Uso correcto: python3 ver_luces.py <año>")
        sys.exit(1)
        
    try:
        year = int(sys.argv[1])
    except ValueError:
        print("[-] Error: El año debe ser un número (ej. 2005).")
        sys.exit(1)

    archivo = os.path.join("descargas_luces", f"luces_{year}.tif")

    if not os.path.exists(archivo):
        print(f"[-] Error: El archivo '{archivo}' no existe. ¿Ya descargaste ese año?")
        sys.exit(1)

    print(f"[+] Abriendo datos de iluminación de {year} ...")

    try:
        with rasterio.open(archivo) as src:
            luz = src.read(1)

        plt.figure(figsize=(10, 8))
        
        # Ajustamos el contraste visual dependiendo del satélite
        if year <= 2013:
            # DMSP-OLS tiene un máximo técnico de 63
            im = plt.imshow(luz, cmap='magma', vmin=0, vmax=63)
            plt.title(f"Luces Nocturnas Dubái - {year} (Satélite DMSP-OLS)\nEscala: 0 a 63", fontsize=14)
        else:
            # VIIRS mide radiancia (suele saturar visualmente alrededor de 10-15 en ciudades)
            im = plt.imshow(luz, cmap='magma', vmin=0, vmax=15)
            plt.title(f"Luces Nocturnas Dubái - {year} (Satélite VIIRS)\nRadiancia", fontsize=14)

        plt.colorbar(im, label='Intensidad de Luz Detectada')
        plt.axis("off")
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"[x] Error al abrir la imagen: {e}")

if __name__ == "__main__":
    main()
