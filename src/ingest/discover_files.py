import shutil
import json
import unicodedata
import re
from pathlib import Path
from rich.console import Console

from src.utils.paths import INGEST_DIR, STAGING_DIR, ensure_directories
from src.utils.hashing import calculate_file_hash

console = Console()

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".csv"}

def sanitize_filename(filename: str) -> str:
    """
    Limpia el nombre del archivo: quita acentos, la letra ñ y caracteres especiales,
    y reemplaza espacios por guiones bajos para evitar errores en motores C/C++.
    """
    # Descompone los caracteres (ej. 'ó' se vuelve 'o' + '´')
    nfd_form = unicodedata.normalize('NFD', filename)
    # Filtra solo los caracteres ASCII (quita los acentos visuales)
    without_accents = nfd_form.encode('ascii', 'ignore').decode('utf-8')
    # Reemplaza todo lo que no sea alfanumérico, punto o guion por guiones bajos
    safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', without_accents)
    return safe_name

def process_ingestion(folder_name: str = None, all_folders: bool = False):
    """Descubre, valida y mueve archivos de ingest a staging sanitizando sus nombres."""
    ensure_directories()
    
    target_dirs = []
    if all_folders:
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
                
                # 1. Obtenemos el nombre base (sin extensión) y lo sanitizamos
                clean_stem = sanitize_filename(file_path.stem)
                
                # 2. Construimos el nombre seguro para staging
                safe_name = f"{clean_stem}_{file_hash[:8]}{file_path.suffix.lower()}"
                dest_path = staging_index / safe_name
                
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
                console.print(f"  [{color}]✔ {file_path.name}[/{color}] -> {status} como {safe_name}")

    if manifest:
        manifest_path = STAGING_DIR / "latest_ingest_manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)
        console.print(f"\n[bold green]Ingesta completada. {len(manifest)} archivos documentados en staging.[/bold green]")
    else:
        console.print("[yellow]No se encontraron archivos compatibles para procesar.[/yellow]")