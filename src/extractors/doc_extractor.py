from pathlib import Path
from docling.document_converter import DocumentConverter
from rich.console import Console

console = Console()

def extract_with_docling(file_path: Path) -> str:
    """
    Extrae el contenido estructural de PDFs y DOCX usando Docling 
    y lo convierte a una representación rica en Markdown.
    """
    console.print(f"    [dim]Iniciando motor Docling para análisis de layout y OCR visual...[/dim]")
    
    # Instanciamos el convertidor. 
    # (Nota: La primera vez que se ejecute podría tardar unos segundos extra 
    # si necesita descargar los modelos locales de layout en tu máquina).
    converter = DocumentConverter()
    
    # Procesamos el documento
    result = converter.convert(file_path)
    
    # Exportamos directamente a Markdown preservando la estructura canónica
    markdown_content = result.document.export_to_markdown()
    
    return markdown_content