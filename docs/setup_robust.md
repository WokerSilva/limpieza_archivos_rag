# Guía de Setup Avanzado: Motor de Visión Local (PaddleOCR)

**ESTADO:** ACTIVO (Para PDFs/PPTs escaneados o basados en imagen).

Este proyecto ha implementado un robustecimiento de grado empresarial para cumplir con el requisito de "mapear texto de imágenes de PPTs y diagramas" 100% de forma local.

## 1. Prerrequisitos del Sistema (Windows Corporativo)

PaddleOCR requiere compiladores de C++ para funcionar. Si la instalación de Python falla, el desarrollador/administrador de TI debe instalar:

* **Microsoft Visual C++ Redistributable** para Visual Studio (versiones recientes).
* (Opcional pero recomendado) **Build Tools para Visual Studio** activando el C++ workload.

## 2. Instalación de Dependencias RAG V2

Ejecute en el entorno virtual:

```bash
pip install paddleocr paddlepaddle opencv-python shapely

```

*(Nota: Si la máquina dispone de tarjeta gráfica NVIDIA compatible con CUDA, instale `paddlepaddle-gpu` en lugar de `paddlepaddle` para triplicar la velocidad de OCR).*

## 3. Funcionamiento Interno del Pipeline Robusto

Al ejecutar `python main.py process`, el sistema detecta un PDF. Ya no intenta leer su "capa de texto". Ahora realiza:

1. **Rasterizado de Página:** PyMuPDF convierte la página en una imagen de alta resolución (300 DPI). Esto garantiza que el motor de IA pueda leer texto pequeño dentro de diagramas.
2. **Deep Learning Inference:** PaddleOCR local analiza la imagen. Detecta diagramas, gráficas y "lee" el texto (OCR computacional).
3. **Mapeo Markdown:** El orquestador recibe el texto, lo ordena de arriba a abajo (orden de lectura de PPT) e inyecta el contenido en el `.md` final.

## 4. Limitaciones Actuales y Futuro

**Implementado (V2.1):**

* ✔ Texto de diagramas, gráficas y PPTs basados en imagen (como tu PDF de prueba).
* ✔ Texto embedded en celdas de tablas escaneadas (se extrae el texto, pero no siempre se preserva la cuadrícula de la tabla como Markdown perfecto en esta V2.1; el texto sí sale completo).

**Futuro (V2.2+):**

* Reconstrucción perfecta de la cuadrícula de tablas escaneadas (requiere el módulo `table` de PaddleOCR, cuya instalación es compleja en Windows local corporativo; se priorizó la extracción del texto en V2.1).
* OCR de escritura humana (aún no implementado).