import fitz # PyMuPDF
import pymupdf4llm
import numpy as np
import cv2
from pathlib import Path
from rapidocr_onnxruntime import RapidOCR
from rich.console import Console

console = Console()

def _spatial_ocr_reconstruction(result) -> str:
    """
    Algoritmo Matemático de Reconstrucción (Eje 2 y Eje 3).
    Toma los resultados brutos del OCR y los reconstruye espacialmente.
    Genera indentaciones (jerarquías) y separación de columnas (tablas)
    basándose en las coordenadas (X, Y) de cada caja de texto.
    """
    if not result:
        return "*[Imagen sin texto detectable]*"

    boxes = []
    for line in result:
        # RapidOCR devuelve: [ [[x,y], [x,y], [x,y], [x,y]], "texto", confianza ]
        coords = line[0]
        text = line[1]
        conf = line[2]
        
        # Filtrar basura visual
        if conf < 0.6: 
            continue
            
        # Extraer el centro en Y para alineación de renglones, y el mínimo en X para la indentación
        x_min = min(c[0] for c in coords)
        y_min = min(c[1] for c in coords)
        y_max = max(c[1] for c in coords)
        y_center = (y_min + y_max) / 2
        
        boxes.append({"x": x_min, "y": y_center, "text": text})

    if not boxes:
        return "*[Imagen sin texto detectable]*"

    # 1. Agrupar por renglones (Tolerancia en el eje Y)
    boxes.sort(key=lambda b: b["y"])
    lines = []
    current_line = []
    last_y = -100

    # Tolerancia de 15 píxeles de desviación vertical para considerar que dos palabras están en la misma línea
    TOLERANCE_Y = 15 

    for b in boxes:
        if abs(b["y"] - last_y) > TOLERANCE_Y and current_line:
            lines.append(current_line)
            current_line = [b]
            last_y = b["y"]
        else:
            current_line.append(b)
            # Actualizamos last_y al promedio para balancear renglones chuecos
            last_y = sum(item["y"] for item in current_line) / len(current_line)
            
    if current_line:
        lines.append(current_line)

    # 2. Reconstrucción Espacial (Indentación y Tablas)
    # Encontrar el margen izquierdo absoluto de la página
    min_page_x = min(b["x"] for b in boxes)
    
    # ¿Cuántos píxeles equivalen a un nivel de jerarquía (Tab)?
    PIXELS_PER_TAB = 40 
    
    spatial_text = ""
    for line in lines:
        line.sort(key=lambda b: b["x"]) # Ordenar de izquierda a derecha
        
        line_str = ""
        last_x = min_page_x
        
        for i, b in enumerate(line):
            # Si es la primera palabra del renglón, calculamos su nivel de jerarquía
            if i == 0:
                indent_level = int((b["x"] - min_page_x) / PIXELS_PER_TAB)
                line_str += "  " * indent_level + b["text"]
            else:
                # Si es una palabra en medio de la línea, medimos la distancia con la palabra anterior
                # Si están muy separadas, inyectamos un salto de columna (útil para tablas en PPTs)
                space_diff = int((b["x"] - last_x) / PIXELS_PER_TAB)
                separator = " \t | \t " if space_diff > 1 else " "
                line_str += separator + b["text"]
                
            # Actualizamos la marca de "último X" sumando una aproximación de lo que midió la palabra
            last_x = b["x"] + (len(b["text"]) * 10) 
            
        spatial_text += line_str + "\n"
        
    return spatial_text

def extract_with_hybrid_engine(file_path: Path) -> str:
    """
    Motor Híbrido V3 (Markdown Nativo + Inteligencia Espacial).
    """
    console.print(f"    [bold cyan]Iniciando motor Híbrido V3 (Nativo + Reconstrucción Espacial)...[/bold cyan]")
    
    try:
        ocr = RapidOCR()
        markdown_content = ""
        doc = fitz.open(file_path)
        total_pages = len(doc)
        
        console.print(f"    [dim]Procesando {total_pages} páginas...[/dim]")
        
        for page_num in range(total_pages):
            page = doc[page_num]
            console.print(f"      [dim]-> Analizando página {page_num + 1}...[/dim]", end="")
            
            page_text = f"### Página {page_num + 1}\n\n"
            
            # 1. EVALUADOR DE TEXTO DIGITAL (Eje 1)
            native_text = page.get_text().strip()
            
            # Si tiene más de 50 caracteres, es un documento digital
            if len(native_text) > 50:
                console.print(" [green]✔ (Markdown Digital Activado)[/green]")
                # Recurrimos al extractor rico para traer Títulos (##) y Listas (-)
                md = pymupdf4llm.to_markdown(str(file_path), pages=[page_num])
                page_text += md
            
            # 2. MOTOR DE VISIÓN ESPACIAL (Eje 2 y 3)
            else:
                console.print(" [yellow]⚠ (Visión Activada -> Mapeando Coordenadas X/Y)[/yellow]")
                
                # Rasterizar a 300 DPI
                mat = page.get_pixmap(dpi=300)
                img_array = np.frombuffer(mat.samples, dtype=np.uint8).reshape((mat.h, mat.w, mat.n))
                
                if mat.n == 4:
                    img_opencv = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
                else:
                    img_opencv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                
                # Extraer cajas de texto
                result, _ = ocr(img_opencv)
                
                # Enviar a nuestro algoritmo matemático para mantener la jerarquía
                spatial_text = _spatial_ocr_reconstruction(result)
                page_text += spatial_text
            
            markdown_content += page_text + "\n\n---\n\n"
            
        doc.close()
        return markdown_content
        
    except Exception as e:
        console.print(f"\n    [bold red]Error crítico en motor Híbrido V3: {str(e)}[/bold red]")
        raise e