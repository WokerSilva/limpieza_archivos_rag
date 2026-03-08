from pathlib import Path
import pymupdf4llm
from rich.console import Console

console = Console()

def extract_with_pymupdf(file_path: Path) -> str:
    """
    Extrae el contenido estructural de PDFs usando PyMuPDF4LLM.
    Es 100% offline, no requiere descargas y es amigable con la memoria RAM.
    """
    console.print(f"    [dim]Iniciando motor PyMuPDF4LLM (Modo Offline/Corporate)...[/dim]")
    
    try:
        # Extrae todo el PDF a un Markdown estructurado
        # Soporta tablas y orden de lectura por defecto.
        md_content = pymupdf4llm.to_markdown(str(file_path))
        return md_content
        
    except Exception as e:
        console.print(f"    [bold red]Error interno en PyMuPDF: {str(e)}[/bold red]")
        raise e