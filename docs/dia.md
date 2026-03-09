¡Excelente análisis de QA (Control de Calidad)! Las imágenes que compartiste son oro molido para un ingeniero de datos porque revelan exactamente los límites de la tecnología actual y nos obligan a subir el nivel de la arquitectura.

He detenido el código, analizado a fondo tus imágenes, el archivo Markdown generado y el estado del arte en extracción *offline*. Tienes toda la razón: la versión actual solucionó el problema del texto plano y la memoria, pero **destruyó el contexto espacial y la semántica compleja**.

Aquí tienes mi análisis forense de los errores y la **Estrategia Maestra V4** para solucionarlos de forma definitiva y profesional.

---

### 🔍 Diagnóstico Forense: ¿Por qué falló nuestro Motor V3?

#### 1. El problema del Organigrama (Imágenes de la PPT vs Terminal)

* **Lo que pasó:** El OCR extrajo perfectamente las palabras (CEO, Finanzas, Manager, Analista), pero las apiló como una lista de supermercado.
* **Por qué pasa:** Nuestro algoritmo asume que la indentación (tabulación) depende del margen izquierdo. En un organigrama centrado, "Manager" y "Analista" pueden tener la misma coordenada X (estar alineados verticalmente), por lo que el algoritmo no les pone sangría. Peor aún, el OCR **no ve las líneas** que conectan las cajas, por lo que la relación padre-hijo se pierde irremediablemente al pasarlo a texto.

#### 2. El problema de la Tabla destruida (Imagen de la tabla Ciencia de Datos vs IA)

* **Lo que pasó:** El OCR leyó de izquierda a derecha saltándose las columnas y mezcló definiciones.
* **Por qué pasa:** El OCR lineal busca renglones. Si no le enseñamos a detectar las "líneas verticales" que separan las columnas, leerá la celda 1 de la fila 1, se cruzará a la celda 2 de la fila 1 y lo unirá todo en una sola oración sin sentido.

#### 3. El problema del Texto Corrupto (Imagen del texto "Dise~no" y "autenticaci´on")

* **Lo que pasó:** PyMuPDF extrajo texto con caracteres separados y extraños.
* **Por qué pasa:** Esto no es culpa del OCR, es culpa del PDF nativo. Muchos PDFs tienen una tabla de fuentes corrupta (CID Font Mapping). Cuando PyMuPDF intenta leer el texto digital subyacente, la letra "ñ" está codificada como "~n" y la "ó" como "´o".

---

### 🧠 La Estrategia Maestra (Hacia un Pipeline Multimodal - V4)

Para que tu Agente LLM pueda responder con precisión a preguntas como *"¿De quién depende el Analista?"* o *"¿Cuál es la diferencia entre ML e IA según la tabla?"*, tenemos que dejar de intentar forzar figuras complejas a texto plano.

Los sistemas RAG de grado corporativo más modernos (como los que usan en OpenAI o Google) utilizan una estrategia de **"Document Layout Analysis (DLA) + Multi-modalidad"**. Esta es la lluvia de ideas y la solución estratégica que te propongo implementar:

#### Estrategia A: Para los Organigramas y Diagramas (Extracción Visual RAG)

Intentar convertir un grafo 2D (organigrama) a Markdown es una mala práctica moderna.

* **La Solución:** Usaremos visión computacional (`OpenCV`) para detectar áreas de la página que sean "Bloques Gráficos" (donde hay muchas formas, líneas de conexión y cajas). En lugar de pasarles el OCR, **el sistema recortará ese diagrama y lo guardará como una imagen** (`organigrama_pag17.png`).
* **El Markdown:** En el archivo `.md`, el sistema inyectará la etiqueta `![Diagrama Organigrama](assets/organigrama_pag17.png)`.
* **¿Por qué es superior?** Porque cuando subas este bundle a un LLM moderno (GPT-4o, Gemini 1.5), estos modelos son **Multimodales**. Leerán el Markdown, verán la imagen del organigrama incrustada, analizarán las líneas visualmente por sí mismos y te responderán con 100% de precisión que el Analista está debajo del Manager.

#### Estrategia B: Para las Tablas (Reconocimiento de Estructura de Tablas - TSR)

No usaremos un OCR lineal para las tablas.

* **La Solución:** Integraremos la librería `img2table` (es ligera y 100% offline). Esta librería escanea la imagen buscando patrones de cuadrículas. Cuando encuentra una, aísla cada celda, le pasa el OCR *solo a esa celda*, y luego reconstruye la matriz matemáticamente.
* **El Markdown:** Te devolverá una estructura perfecta: `| Área | ¿Qué hace? | Ejemplo |`.

#### Estrategia C: Análisis por "Bloques", no por "Páginas" (El fin del texto corrupto)

El mayor defecto de nuestro código anterior era que evaluaba la página entera.

* **La Solución:** Implementaremos un motor de reglas.
1. PyMuPDF lee el texto de un bloque. Si el texto tiene una alta tasa de "basura" (detectaremos patrones como `~n`, `´o`), el sistema rechaza el texto digital de ese bloque y **fuerza el OCR** solo para ese pedazo, reparando los acentos.
2. Si el bloque es una tabla, se va a `img2table`.
3. Si el bloque es un diagrama, se recorta como imagen.
4. Si es texto normal, se guarda en Markdown.



---

### 📋 Conclusión y Siguientes Pasos

Si intentamos hacer todo esto en un solo archivo `doc_extractor.py` gigante, el código será inmanejable.

Para llegar a este nivel de RAG Avanzado, necesitamos estructurar tu código usando la arquitectura que ya vi que empezaste a armar en tu carpeta `src/` (con módulos para OCR, normalización, etc.).

**El plan de ataque técnico:**

1. Instalar dependencias de visión (`pip install img2table`).
2. Crear un script que extraiga imágenes y diagramas a una carpeta `assets/` vinculada a cada Markdown.
3. Actualizar la lógica para ensamblar el Markdown combinando: Texto Limpio + Tablas Estructuradas + Referencias a Imágenes



¡Decisión de Arquitecto de Software Senior! Detenerse a refactorizar y modularizar antes de inyectar nueva complejidad (como `img2table` y la extracción de imágenes multimodales) es exactamente lo que evita que un proyecto se convierta en "código espagueti".

Al ver tu estructura de carpetas, tienes un esqueleto hermoso preparado. Vamos a desarmar el monstruoso `doc_extractor.py` y a repartir sus responsabilidades en las carpetas `ocr` y `normalize`. De esta forma, cada archivo hará una sola cosa y la hará excelente.

---

### 🧱 Fase 1: Modularización del Código Actual (Preparando el terreno)

Vamos a crear tres archivos nuevos para separar el Procesamiento de Imagen, la Normalización Espacial y la Extracción.

#### 1. El Motor OCR (`src/ocr/vision.py`)

Este módulo se encargará única y exclusivamente de transformar páginas en imágenes y pasarlas por el modelo de IA. Crea el archivo **`src/ocr/vision.py`** y pega esto:

```python
import numpy as np
import cv2
from rapidocr_onnxruntime import RapidOCR

class VisionEngine:
    def __init__(self):
        # Inicializamos el modelo una sola vez en memoria
        self.ocr = RapidOCR()

    def rasterize_and_read(self, fitz_page, dpi=300):
        """
        Convierte una página de PyMuPDF en imagen OpenCV y ejecuta el OCR.
        Devuelve el resultado crudo del modelo.
        """
        mat = fitz_page.get_pixmap(dpi=dpi)
        img_array = np.frombuffer(mat.samples, dtype=np.uint8).reshape((mat.h, mat.w, mat.n))
        
        # Manejo seguro de canales de color (RGB vs RGBA)
        if mat.n == 4:
            img_opencv = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
        else:
            img_opencv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
        result, _ = self.ocr(img_opencv)
        return result

```

#### 2. El Normalizador Espacial (`src/normalize/spatial.py`)

Aquí vivirá toda la matemática compleja para calcular márgenes, tabulaciones y saltos de línea. Crea el archivo **`src/normalize/spatial.py`** y pega esto:

```python
def reconstruct_spatial_text(ocr_result, pixels_per_tab=40, tolerance_y=15) -> str:
    """
    Toma los resultados brutos del OCR y los reconstruye espacialmente.
    Genera indentaciones (jerarquías) y separación de columnas (tablas)
    basándose en las coordenadas (X, Y) de cada caja de texto.
    """
    if not ocr_result:
        return "*[Imagen sin texto detectable]*"

    boxes = []
    for line in ocr_result:
        coords = line[0]
        text = line[1]
        conf = line[2]
        
        if conf < 0.6: 
            continue
            
        x_min = min(c[0] for c in coords)
        y_min = min(c[1] for c in coords)
        y_max = max(c[1] for c in coords)
        y_center = (y_min + y_max) / 2
        
        boxes.append({"x": x_min, "y": y_center, "text": text})

    if not boxes:
        return "*[Imagen sin texto detectable]*"

    # Agrupar por renglones
    boxes.sort(key=lambda b: b["y"])
    lines = []
    current_line = []
    last_y = -100

    for b in boxes:
        if abs(b["y"] - last_y) > tolerance_y and current_line:
            lines.append(current_line)
            current_line = [b]
            last_y = b["y"]
        else:
            current_line.append(b)
            last_y = sum(item["y"] for item in current_line) / len(current_line)
            
    if current_line:
        lines.append(current_line)

    # Reconstrucción Espacial
    min_page_x = min(b["x"] for b in boxes)
    spatial_text = ""
    
    for line in lines:
        line.sort(key=lambda b: b["x"]) 
        line_str = ""
        last_x = min_page_x
        
        for i, b in enumerate(line):
            if i == 0:
                indent_level = int((b["x"] - min_page_x) / pixels_per_tab)
                line_str += "  " * indent_level + b["text"]
            else:
                space_diff = int((b["x"] - last_x) / pixels_per_tab)
                separator = " \t | \t " if space_diff > 1 else " "
                line_str += separator + b["text"]
                
            last_x = b["x"] + (len(b["text"]) * 10) 
            
        spatial_text += line_str + "\n"
        
    return spatial_text

```

#### 3. El Extractor Refactorizado (`src/extractors/doc_extractor.py`)

Ahora que le quitamos la carga pesada, este archivo se convierte en un simple **director de orquesta**. Reemplaza tu **`src/extractors/doc_extractor.py`** actual con esto:

```python
import fitz # PyMuPDF
import pymupdf4llm
from pathlib import Path
from rich.console import Console

# Importamos nuestros nuevos módulos
from src.ocr.vision import VisionEngine
from src.normalize.spatial import reconstruct_spatial_text

console = Console()

def extract_with_hybrid_engine(file_path: Path) -> str:
    """
    Motor Híbrido Modularizado.
    Delega la visión a src.ocr y la matemática a src.normalize.
    """
    console.print(f"    [bold cyan]Iniciando motor Híbrido (Arquitectura Modular)...[/bold cyan]")
    
    try:
        vision_engine = VisionEngine()
        markdown_content = ""
        doc = fitz.open(file_path)
        total_pages = len(doc)
        
        console.print(f"    [dim]Procesando {total_pages} páginas...[/dim]")
        
        for page_num in range(total_pages):
            page = doc[page_num]
            console.print(f"      [dim]-> Analizando página {page_num + 1}...[/dim]", end="")
            
            page_text = f"### Página {page_num + 1}\n\n"
            native_text = page.get_text().strip()
            
            # 1. Flujo de Texto Digital
            if len(native_text) > 50:
                console.print(" [green]✔ (Markdown Digital Activado)[/green]")
                md = pymupdf4llm.to_markdown(str(file_path), pages=[page_num])
                page_text += md
                
            # 2. Flujo de Visión Espacial
            else:
                console.print(" [yellow]⚠ (Visión Activada -> OCR Espacial)[/yellow]")
                ocr_result = vision_engine.rasterize_and_read(page)
                spatial_text = reconstruct_spatial_text(ocr_result)
                page_text += spatial_text
            
            markdown_content += page_text + "\n\n---\n\n"
            
        doc.close()
        return markdown_content
        
    except Exception as e:
        console.print(f"\n    [bold red]Error crítico en Extractor Documental: {str(e)}[/bold red]")
        raise e

```

---

### 🚀 Validación de la Refactorización

Ejecuta tu pipeline para comprobar que todo sigue funcionando igual, pero ahora con el código elegantemente separado:

```bash
python main.py process

```

Si el proceso termina sin errores, significa que **nuestro esqueleto modular es sólido**.

En cuanto me confirmes que esto funciona, daremos el salto a la **Estrategia Multimodal (V4)**: Usaremos nuestra nueva carpeta `src/renderers/` para guardar imágenes de los diagramas complejos y modificaremos `src/ocr/` para integrar `img2table`. ¿Listo para probar esta estructura?