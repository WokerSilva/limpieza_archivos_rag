import typer
from rich.console import Console
from dotenv import load_dotenv
import os
from src.ingest.discover_files import process_ingestion


# Cargar variables de entorno
load_dotenv()

app = typer.Typer(
    name="RAG Document Cleaner",
    help="Pipeline local de limpieza, extracción y empaquetado documental para LLMs.",
    add_completion=False,
)
console = Console()

@app.command()
def ingest(
    folder: str = typer.Option(None, "--folder", "-f", help="Carpeta específica dentro de data/ingest/ para procesar."),
    all: bool = typer.Option(False, "--all", "-a", help="Procesa todos los archivos en data/ingest/")
):
    """
    Fase 1 del pipeline: Ingesta, clasifica y mueve archivos a staging.
    """
    console.print("[bold blue]Iniciando proceso de ingesta...[/bold blue]")
    if not folder and not all:
        console.print("[bold red]Debes especificar una carpeta con --folder o usar --all.[/bold red]")
        raise typer.Exit(code=1)
    
    # Aquí irá la lógica de src/ingest/
    console.print("[green]Ingesta simulada completada.[/green]")

@app.command()
def process():
    """
    Fase 2 del pipeline: Extrae, normaliza y renderiza los archivos desde staging.
    """
    console.print("[bold blue]Iniciando procesamiento y extracción (Docling/Pandas)...[/bold blue]")
    # Aquí irá la lógica de src/extractors/ y src/renderers/
    console.print("[green]Procesamiento simulado completado.[/green]")

@app.command()
def bundle(
    folder: str = typer.Argument(..., help="Nombre de la carpeta de lotes a empaquetar.")
):
    """
    Fase 3 del pipeline: Une archivos Markdown calculando límites para GPT.
    """
    console.print(f"[bold blue]Evaluando archivos en lote: {folder}...[/bold blue]")
    # Aquí irá la lógica interactiva de src/bundle/
    console.print("[green]Bundling simulado completado.[/green]")

@app.command()
def ingest(
    folder: str = typer.Option(None, "--folder", "-f", help="Carpeta específica dentro de data/ingest/ para procesar."),
    all: bool = typer.Option(False, "--all", "-a", help="Procesa todas las carpetas en data/ingest/")
):
    """
    Fase 1 del pipeline: Ingesta, clasifica y mueve archivos a staging.
    """
    console.print("[bold blue]Iniciando proceso de ingesta...[/bold blue]")
    if not folder and not all:
        console.print("[bold red]Debes especificar una carpeta con --folder o usar --all.[/bold red]")
        raise typer.Exit(code=1)
    
    # Ejecutamos la lógica real
    process_ingestion(folder_name=folder, all_folders=all)

if __name__ == "__main__":
    app()