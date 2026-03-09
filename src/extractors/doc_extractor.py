import os
import fitz # PyMuPDF puro
import numpy as np
import cv2
from pathlib import Path
from paddleocr import PaddleOCR
from rich.console import Console

console = Console()

# FIX WINDOWS: Desactivar telemetría de PaddlePaddle si aplica
os.environ['FLAGS_eager_delete_tensor_gb'] = "0.0"

def extract_with_paddle_vision(file_path: Path) -> str:
    """
    Extractor ROBUSTO V2.
    Utiliza PyMuPDF para rasterizar páginas y PaddleOCR local para 
    "leer" texto embedded en imágenes, diagramas y tablas escaneadas.
    Es 100% offline y seguro.
    """
    console.print(f"    [bold yellow]Iniciando motor de Visión Local (PaddleOCR v2.7)...[/bold yellow]")
    console.print(f"    [dim]Dependencias de C++ cargadas. Consumo de RAM: Mediano.[/dim]")
    
    # Inicializar PaddleOCR (usando CPU, idioma español).
    # La primera vez descargará modelos ligeros locales (~150MB).
    ocr = PaddleOCR(use_angle_cls=True, lang='es', use_gpu=False, show_log=False)
    
    markdown_content = ""
    
    try:
        # Abrir el PDF con PyMuPDF puro
        doc = fitz.open(file_path)
        total_pages = len(doc)
        
        console.print(f"    [dim]Procesando {total_pages} páginas visuales...[/dim]")
        
        for page_num, page in enumerate(doc):
            console.print(f"      [dim]-> OCR en página {page_num+1}...[/dim]")
            
            # 1. Rasterizar la página: Convertirla a una imagen de alta resolución (DPI 300)
            # Esto es clave para que el OCR lea diagramas pequeños de PPT.
            mat = page.get_pixmap(dpi=300)
            
            # 2. Convertir Pixmap de PyMuPDF a formato OpenCv (BGR) para PaddleOCR
            # Leemos los bytes crudos y reconstruimos la imagen en memoria.
            img_array = np.frombuffer(mat.samples, dtype=np.uint8).reshape((mat.h, mat.w, mat.n))
            img_opencv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # 3. Ejecutar el OCR local en la imagen de la página
            result = ocr.ocr(img_opencv, cls=True)
            
            # 4. Procesar el resultado del OCR y armar el Markdown
            page_text = f"\n\n### Página {page_num + 1}\n\n"
            
            # PaddleOCR devuelve una lista de listas [[box, (text, score)]]
            if result[0]: # Si detectó texto
                # Ordenar los bloques de texto de arriba a abajo, izquierda a derecha
                # para mantener el orden de lectura de la PPT.
                texts_ordered = sorted(result[0], key=lambda x: (x[0][0][1], x[0][0][0]))
                
                for line in texts_ordered:
                    text = line[1][0] # El texto detectado
                    confidence = line[1][1] # La confianza de la IA
                    
                    # Filtro de confianza opcional (ej. ignorar texto < 60%)
                    if confidence > 0.6:
                        page_text += f"{text} "
            
            markdown_content += page_text + "\n"
            
        doc.close()
        return markdown_content
        
    except Exception as e:
        console.print(f"    [bold red]Error crítico en motor de visión PaddleOCR: {str(e)}[/bold red]")
        # Fallback de emergencia si PaddleOCR explota por memoria en Windows
        console.print(f"    [bold red]✖ Intento colapsado. Revisa recursos de RAM corporativos.[/bold red]\n")
        raise e