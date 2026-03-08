import json
from pathlib import Path
from rich.console import Console

from src.utils.paths import STAGING_DIR, OUTPUT_DIR
from src.extractors.doc_extractor import extract_with_pymupdf

console = Console()

def process_staging_files():
    """Lee el manifiesto de staging y procesa cada archivo hacia output."""
    manifest_path = STAGING_DIR / "latest_ingest_manifest.json"
    
    if not manifest_path.exists():
        console.print("[bold red]No se encontró el manifiesto de ingesta. Ejecuta 'python main.py ingest --all' primero.[/bold red]")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    if not manifest:
        console.print("[yellow]El manifiesto está vacío. No hay archivos para procesar.[/yellow]")
        return

    md_out_dir = OUTPUT_DIR / "individuales" / "md"

    console.print(f"[bold blue]Iniciando procesamiento de {len(manifest)} archivos...[/bold blue]\n")

    for item in manifest:
        staging_name = item["staging_name"]
        file_path = STAGING_DIR / "originals_index" / staging_name
        ext = item["extension"]

        if not file_path.exists():
            console.print(f"[red]Archivo no encontrado en staging: {staging_name}[/red]")
            continue

        console.print(f"[bold cyan]Procesando:[/bold cyan] {staging_name}")

        try:
            # Fase 3: Procesamiento de Documentos (PDF, DOCX)
            if ext in [".pdf", ".docx"]:
                md_content = extract_with_pymupdf(file_path)
                
                # Construir el nombre de salida (ej. Titulacion_hash.md)
                out_name = f"{Path(staging_name).stem}.md"
                out_path = md_out_dir / out_name
                
                # Inyectar trazabilidad al inicio del Markdown
                header = f"---\nOrigen: {item['original_name']}\nCarpeta: {item['original_folder']}\nHash: {item['hash']}\n---\n\n"
                
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(header + md_content)
                    
                console.print(f"  [green]✔ Extracción completada. Guardado en: {out_name}[/green]\n")
                
            # Fase 4: Preparación para Datos Tabulares
            elif ext in [".xlsx", ".csv"]:
                console.print(f"  [yellow]⚙️ Archivo tabular detectado. Se procesará mediante flujos de Pandas en la Fase 4.[/yellow]\n")
            
            else:
                console.print(f"  [yellow]⚠️ Extensión no soportada en este flujo: {ext}[/yellow]\n")
        
        except Exception as e:
            console.print(f"  [bold red]✖ Error crítico procesando {staging_name}: {str(e)}[/bold red]\n")

    console.print("[bold green]Procesamiento masivo completado.[/bold green]")