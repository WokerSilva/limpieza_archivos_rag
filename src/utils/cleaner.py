import shutil
from pathlib import Path
from rich.console import Console

from src.utils.paths import STAGING_DIR, OUTPUT_DIR, CACHE_DIR, ensure_directories

console = Console()

def clean_environment():
    """
    Elimina recursivamente el contenido de las carpetas de trabajo 
    (staging, output, cache) y recrea la estructura base vacía.
    Nunca toca la carpeta 'ingest'.
    """
    dirs_to_clean = [STAGING_DIR, OUTPUT_DIR, CACHE_DIR]
    
    for directory in dirs_to_clean:
        if directory.exists():
            try:
                # Borra la carpeta y todo su contenido
                shutil.rmtree(directory)
                console.print(f"  [green]✔ Limpiado: {directory.name}/[/green]")
            except Exception as e:
                console.print(f"  [bold red]✖ Error limpiando {directory.name}: {str(e)}[/bold red]")
    
    # Inmediatamente recreamos la estructura de carpetas vacía
    ensure_directories()
    console.print("\n[bold green]¡Entorno reiniciado exitosamente! Todo listo para una nueva ingesta.[/bold green]")