# Monitoreo Satelital del Crecimiento Urbano (Dubái 2000–2026)

**Materia:** Procesamiento de Imágenes Satelitales  
**Institución:** Instituto Tecnológico de Buenos Aires (ITBA)  
**Alumno:** Augusto Cicciomessere  

---

## 📌 Descripción del Proyecto

Este repositorio contiene las herramientas de descarga, inspección y procesamiento satelital desarrolladas para analizar la expansión urbana histórica de Dubái (Emiratos Árabes Unidos) en el período **2000–2026**.

El flujo de trabajo cubre **tres metodologías de análisis**:
1. **Suma Espectral de Bandas RGB (`analizar_suma_rgb`):** Detección de superficie construida mediante la suma de canales visibles ($R + G + B$) e intervalo de corte para separar la ciudad del agua y las dunas de arena.
2. **Índice IBI (*Index-based Built-up Index*, `analizar_ibi`):** Índice espectral compuesto que combina NDBI, MNDWI y SAVI para aislar construcciones en entornos áridos complejos.
3. **Emisión de Luces Nocturnas (*Nighttime Lights*, `analizar_luces`):** Monitoreo de la expansión mediante radiometría nocturna (sensores DMSP-OLS y VIIRS) con umbrales calibrados por sensor.

Adicionalmente, se incluyen **scripts interactivos de inspección rápida (`ver_*`)** para examinar de manera visual e individual los rasters GeoTIFF descargados sin necesidad de correr el análisis completo.

---

## ⚙️ Requisitos y Configuración del Entorno

### 1. Requisitos Previos
- Python 3.9 o superior.
- Una cuenta de **Google Earth Engine (GEE)** con un proyecto de Google Cloud habilitado. Si aún no tienes uno, puedes habilitarlo de forma gratuita en [Google Earth Engine](https://earthengine.google.com/).

### 2. Creación del Entorno Virtual e Instalación de Dependencias

Se recomienda utilizar un entorno virtual para aislar las librerías:

```bash
# Situarse en el directorio del proyecto
cd /ruta/al/proyecto/script_satelital

# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# En macOS / Linux:
source venv/bin/activate
# En Windows:
# .\venv\Scripts\activate

# Instalar dependencias requeridas
pip install --upgrade pip
pip install earthengine-api geemap rasterio numpy matplotlib
```

---

## 🔑 Configuración de Google Earth Engine (Tu Propio Proyecto)

Los scripts de descarga interactúan con la API de Google Earth Engine a través del cliente oficial de Python y `geemap`.

### 1. Autenticación
La primera vez que ejecutes cualquiera de los scripts de descarga, deberás autorizar el acceso a tu cuenta de Google:
```bash
python3 -c "import ee; ee.Authenticate()"
```

### 2. Configurar tu Proyecto de Google Cloud / Earth Engine
En los scripts de descarga (`descargar_imagenes.py`, `descargar_ibi.py` y `descargar_luces.py`), ubica la línea de inicialización:

```python
ee.Initialize(project='imposing-carver-505921-e0')
```

> [!IMPORTANT]
> **Reemplaza `'imposing-carver-505921-e0'` por el ID de tu propio proyecto de GEE / Google Cloud** (por ejemplo: `ee.Initialize(project='tu-id-de-proyecto')`).

---

## 🗺️ Región de Interés (ROI) y Período Temporal

Todos los scripts de descarga utilizan la misma Región de Interés (Dubái y su frente costero):
- **Vértices (Longitud, Latitud):**
  - Esquina Noroeste: `[54.8355, 25.7749]`
  - Esquina Noreste: `[55.8235, 25.7749]`
  - Esquina Sureste: `[55.8235, 24.8351]`
  - Esquina Suroeste: `[54.8355, 24.8351]`
- **Resolución espacial de exportación:** 150 metros por píxel.
- **Rango temporal:** Años 2000 a 2026.

---

## 🔍 Scripts de Inspección Rápida (`ver_*`)

Antes o después de procesar las series temporales completas, puedes inspeccionar directamente los archivos GeoTIFF individuales en pantalla mediante los siguientes scripts auxiliares:

### 1. Visor Genérico de GeoTIFFs (`ver_tiff.py`)
Permite visualizar cualquier archivo `.tif` del proyecto. Detecta automáticamente si el archivo tiene 3 bandas (RGB diurno) o 1 sola banda (índices o luces):

```bash
# Visualizar un mosaico RGB diurno:
python3 ver_tiff.py descargas_roi/imagen_2020.tif

# Visualizar un raster monocanal (IBI o Luces):
python3 ver_tiff.py descargas_ibi/ibi_2020.tif
python3 ver_tiff.py descargas_luces/luces_2020.tif
```
- **RGB ($\ge 3$ bandas):** Aplica normalización de contraste visual y renderiza la imagen a color.
- **Monobanda (1 banda):** Renderiza en escala de grises con barra de valores de píxel.

### 2. Visor Especializado de Índice IBI (`ver_ibi.py`)
Permite examinar el mapa del índice IBI de un año específico, recortando los valores al rango analítico $[-2.0, 1.5]$ con el mapa de colores `RdBu_r`:

```bash
python3 ver_ibi.py <año>
# Ejemplo:
python3 ver_ibi.py 2015
```
- **Rango:** $-2.0$ (Agua y arena) hasta $+1.5$ (Estructuras urbanas y edificadas).

### 3. Visor Especializado de Luces Nocturnas (`ver_luces.py`)
Permite inspeccionar la emisión lumínica nocturna de un año específico, adaptando automáticamente la paleta y la escala de visualización según el satélite del período:

```bash
python3 ver_luces.py <año>
# Ejemplos:
python3 ver_luces.py 2008   # Satélite DMSP-OLS (escala 0 a 63)
python3 ver_luces.py 2022   # Satélite VIIRS (radiancia, escala 0 a 15)
```
- **Paleta de color:** `magma` con barra de intensidad de iluminación.

---

## 🚀 Guía de Ejecución: Análisis Paso a Paso

> [!TIP]
> **Prerrequisito Común:** Tanto el análisis de IBI como el de Luces Nocturnas utilizan como fondo visual los mosaicos diurnos descargados en `descargas_roi/`. Por ende, **se recomienda ejecutar primero la descarga de imágenes RGB (`descargar_imagenes.py`)**.

```
                           ┌───────────────────────────┐
                           │   descargar_imagenes.py   │  ──> descargas_roi/
                           └─────────────┬─────────────┘
                                         │ (Fondo base RGB)
         ┌───────────────────────────────┼───────────────────────────────┐
         │                               │                               │
         ▼                               ▼                               ▼
┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐
│analizar_suma_rgb │           │  descargar_ibi   │           │ descargar_luces  │
└──────────────────┘           └─────────┬────────┘           └─────────┬────────┘
                                         ▼                              ▼
                               ┌──────────────────┐           ┌──────────────────┐
                               │   analizar_ibi   │           │  analizar_luces  │
                               └──────────────────┘           └──────────────────┘
```

---

### 1. Análisis por Suma de Bandas RGB (`analizar_suma_rgb`)

#### Fundamento Teórico
En el desierto, la arena tiene una fuerte reflectancia en el canal Rojo. Las estructuras artificiales (hormigón, asfalto, metales y techos) reflejan de manera más homogénea en el espectro visible, incrementando la respuesta de la suma $R + G + B$. Al acotar la suma dentro de un intervalo empírico calibrado, se aísla el tejido urbano evitando el agua (valores bajos) y las dunas hiperreflectantes (valores altos).

#### Paso 1.1: Descarga de Imágenes RGB
Descarga mosaicos anuales medianos TOA de Landsat 7 (2000–2012) y Landsat 8 (2013–2026) con bandas Rojo, Verde y Azul:

```bash
python3 descargar_imagenes.py
```
- **Salida:** Archivos `imagen_YYYY.tif` en la carpeta `descargas_roi/`.

#### Paso 1.2: Procesamiento y Cálculo de Expansión
Calcula la suma $R + G + B$, aplica el intervalo $[0.5, 0.7]$, mantiene una máscara acumulativa y calcula el área urbana en $\text{km}^2$:

```bash
python3 analizar_suma_rgb.py
```
- **Resultados generados:**
  - Mapas anuales en `ciudad_rgb_intervalo/mapa_YYYY.png`.
  - Gráfico evolutivo temporal: `grafico_crecimiento_rgb_intervalo.png`.

---

### 2. Análisis por Índice Urbano IBI (`analizar_ibi`)

#### Fundamento Teórico
El **IBI** (*Index-based Built-up Index*, Xu 2008) es un índice diseñado para extraer áreas urbanas integrando tres índices espectrales normalizados:
- **NDBI** (*Normalized Difference Built-up Index*): Destaca construcciones mediante SWIR y NIR.
- **SAVI** (*Soil-Adjusted Vegetation Index*): Corrige y suprime la respuesta del suelo árido y la vegetación.
- **MNDWI** (*Modified Normalized Difference Water Index*): Suprime la respuesta de cuerpos de agua.

$$\text{IBI} = \frac{\text{NDBI} - \frac{\text{SAVI} + \text{MNDWI}}{2}}{\text{NDBI} + \frac{\text{SAVI} + \text{MNDWI}}{2}}$$

#### Paso 2.1: Cálculo y Descarga del IBI en GEE
Calcula sobre colecciones Landsat las bandas necesarias ($Green, Red, NIR, SWIR_1$), evalúa la fórmula del IBI en los servidores de Earth Engine y exporta el raster resultante:

```bash
python3 descargar_ibi.py
```
- **Salida:** Archivos `ibi_YYYY.tif` en la carpeta `descargas_ibi/`.

#### Paso 2.2: Procesamiento del IBI y Cálculo de Superficie
Aplica el intervalo $[-2.0, 1.5]$ sobre el raster de IBI para segmentar el tejido edificado, acumula la huella urbana histórica y superpone la máscara sobre la imagen base RGB:

```bash
python3 analizar_ibi.py
```
- **Resultados generados:**
  - Mapas anuales en `ciudad_ibi/mapa_ibi_YYYY.png`.
  - Gráfico evolutivo temporal: `grafico_crecimiento_ibi_ajustado.png`.

---

### 3. Análisis por Luces Nocturnas (`analizar_luces`)

#### Fundamento Teórico
Monitorea la expansión del tejido urbano y la electrificación a través de sensores nocturnos satelitales:
- **2000–2013 (DMSP-OLS):** Sensor *Operational Linescan System*, banda `stable_lights` (escala digital de brillo 0 a 63).
- **2014–2026 (VIIRS-DNB):** Sensor *Day/Night Band*, banda `avg_rad` (radiancia en $\text{nW}\cdot\text{cm}^{-2}\cdot\text{sr}^{-1}$).

#### Paso 3.1: Descarga de Rasters Nocturnos
Descarga los productos satelitales anuales de NOAA correspondientes a cada sensor:

```bash
python3 descargar_luces.py
```
- **Salida:** Archivos `luces_YYYY.tif` en la carpeta `descargas_luces/`.

#### Paso 3.2: Procesamiento con Umbrales Ajustados
Aplica umbrales diferenciados y calibrados según el sensor (umbral $> 35$ para DMSP-OLS y $> 10$ para VIIRS), acumula la superficie iluminada histórica y calcula el área total en $\text{km}^2$:

```bash
python3 analizar_luces.py
```
- **Resultados generados:**
  - Mapas anuales en `ciudad_luces_ajustado/mapa_luces_YYYY.png`.
  - Gráfico evolutivo temporal: `grafico_crecimiento_luces_ajustado.png`.

---

## 📁 Estructura de Directorios y Archivos

```
script_satelital/
│
├── descargar_imagenes.py           # Descarga de mosaicos ópticos RGB (Landsat 7 y 8)
├── analizar_suma_rgb.py            # Análisis de expansión por suma RGB (intervalo 0.5 a 0.7)
│
├── descargar_ibi.py                # Cálculo y descarga del índice IBI en GEE
├── analizar_ibi.py                 # Segmentación por IBI y cálculo de área (-2.0 a 1.5)
│
├── descargar_luces.py              # Descarga de sensores nocturnos (DMSP-OLS y VIIRS)
├── analizar_luces.py               # Segmentación por luces (DMSP > 35, VIIRS > 10)
│
├── ver_tiff.py                     # Visor genérico por terminal para cualquier GeoTIFF
├── ver_ibi.py                      # Visor interactivo especializado para GeoTIFFs de IBI
├── ver_luces.py                    # Visor interactivo especializado para GeoTIFFs de Luces
│
├── descargas_roi/                  # GeoTIFFs RGB descargados (imagen_YYYY.tif)
├── descargas_ibi/                  # GeoTIFFs IBI descargados (ibi_YYYY.tif)
├── descargas_luces/                # GeoTIFFs de luces descargados (luces_YYYY.tif)
│
├── ciudad_rgb_intervalo/           # Mapas anuales de la Suma RGB
├── ciudad_ibi/                     # Mapas anuales del índice IBI
├── ciudad_luces_ajustado/          # Mapas anuales de Luces Nocturnas
│
├── grafico_crecimiento_rgb_intervalo.png
├── grafico_crecimiento_ibi_ajustado.png
├── grafico_crecimiento_luces_ajustado.png
└── README.md
```

---

## 👨‍💻 Información Académica

- **Alumno:** Augusto Cicciomessere
- **Materia:** Procesamiento de Imágenes Satelitales
- **Institución:** Instituto Tecnológico de Buenos Aires (ITBA)
