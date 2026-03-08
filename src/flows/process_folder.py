import json
from pathlib import Path
from rich.console import Console

from src.utils.paths import STAGING_DIR, OUTPUT_DIR
from src.extractors.doc_extractor import extract_with_pymupdf
# NUEVO: Importamos el extractor de hojas de cálculo
from src.extractors.spreadsheet import process_spreadsheet 

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
    json_out_dir = OUTPUT_DIR / "individuales" / "json"

    console.print(f"[bold blue]Iniciando procesamiento de {len(manifest)} archivos...[/bold blue]\n")

    for item in manifest:
        staging_name = item["staging_name"]
        file_path = STAGING_DIR / "originals_index" / staging_name
        ext = item["extension"]

        if not file_path.exists():
            console.print(f"[red]Archivo no encontrado en staging: {staging_name}[/red]")
            continue

        console.print(f"[bold cyan]Procesando:[/bold cyan] {staging_name}")

        # Inyectar trazabilidad al inicio de todos los archivos
        header = f"---\nOrigen: {item['original_name']}\nCarpeta: {item['original_folder']}\nHash: {item['hash']}\n---\n\n"
        base_out_name = Path(staging_name).stem

        try:
            # FASE 3: Documentos de Texto (PDF, DOCX)
            if ext in [".pdf", ".docx"]:
                md_content = extract_with_pymupdf(file_path)
                
                out_path = md_out_dir / f"{base_out_name}.md"
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(header + md_content)
                    
                console.print(f"  [green]✔ Extracción PDF/DOCX completada. Guardado en: {out_path.name}[/green]\n")
                
            # FASE 4: Datos Tabulares (Excel, CSV)
            elif ext in [".xlsx", ".csv"]:
                results = process_spreadsheet(file_path)
                
                # 1. Guardar el Markdown (Resumen o Tabla Completa)
                md_path = md_out_dir / f"{base_out_name}.md"
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(header + results["markdown"])
                
                # 2. Guardar el JSON (Estructura de auditoría y análisis)
                json_path = json_out_dir / f"{base_out_name}.json"
                # Añadimos los metadatos al JSON también
                final_json = {
                    "metadata": {
                        "origen": item["original_name"],
                        "hash": item["hash"]
                    },
                    "data": results["json_data"]
                }
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(final_json, f, indent=4, ensure_ascii=False)
                    
                console.print(f"  [green]✔ Extracción Tabular completada. Generados: .md y .json[/green]\n")
            
            else:
                console.print(f"  [yellow]⚠️ Extensión no soportada en este flujo: {ext}[/yellow]\n")
        
        except Exception as e:
            console.print(f"  [bold red]✖ Error crítico procesando {staging_name}: {str(e)}[/bold red]\n")

    console.print("[bold green]Procesamiento masivo completado.[/bold green]")