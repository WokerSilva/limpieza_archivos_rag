import shutil
import json
from pathlib import Path
from rich.console import Console

from src.utils.paths import INGEST_DIR, STAGING_DIR, ensure_directories
from src.utils.hashing import calculate_file_hash

console = Console()

# Extensiones permitidas en esta fase V1
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".csv"}

def process_ingestion(folder_name: str = None, all_folders: bool = False):
    """Descubre, valida y mueve archivos de ingest a staging."""
    ensure_directories()
    
    target_dirs = []
    if all_folders:
        # Iterar sobre todas las subcarpetas de ingest/
        target_dirs = [d for d in INGEST_DIR.iterdir() if d.is_dir()]
    elif folder_name:
        target_dir = INGEST_DIR / folder_name
        if target_dir.exists() and target_dir.is_dir():
            target_dirs.append(target_dir)
        else:
            console.print(f"[bold red]La carpeta '{folder_name}' no existe en data/ingest/.[/bold red]")
            return

    if not target_dirs:
        console.print("[yellow]No se encontraron carpetas válidas para procesar en data/ingest/.[/yellow]")
        return

    manifest = []
    staging_index = STAGING_DIR / "originals_index"

    for directory in target_dirs:
        console.print(f"[bold blue]Escaneando directorio: {directory.name}...[/bold blue]")
        
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                file_hash = calculate_file_hash(file_path)
                # Inyectamos el inicio del hash al nombre para garantizar unicidad en staging
                safe_name = f"{file_path.stem}_{file_hash[:8]}{file_path.suffix.lower()}"
                dest_path = staging_index / safe_name
                
                # Control de Idempotencia: Si ya está en staging, no copiamos de nuevo
                if not dest_path.exists():
                    shutil.copy2(file_path, dest_path)
                    status = "Copiado a staging"
                    color = "green"
                else:
                    status = "Ya existe en staging (Omitido)"
                    color = "yellow"

                manifest.append({
                    "original_name": file_path.name,
                    "original_folder": directory.name,
                    "staging_name": safe_name,
                    "hash": file_hash,
                    "extension": file_path.suffix.lower(),
                    "status": status
                })
                console.print(f"  [{color}]✔ {file_path.name}[/{color}] -> {status}")

    # Escribir el manifiesto de la ingesta
    if manifest:
        manifest_path = STAGING_DIR / "latest_ingest_manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)
        console.print(f"\n[bold green]Ingesta completada. {len(manifest)} archivos documentados en staging.[/bold green]")
        console.print(f"[dim]Manifiesto guardado en: {manifest_path}[/dim]")
    else:
        console.print("[yellow]No se encontraron archivos compatibles para procesar.[/yellow]")