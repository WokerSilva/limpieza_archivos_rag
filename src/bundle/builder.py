import os
import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

from src.utils.paths import OUTPUT_DIR

console = Console()

def create_bundles():
    """
    Lee los markdowns individuales, calcula métricas, solicita al usuario 
    la partición y genera los bundles con un índice inyectado.
    """
    md_in_dir = OUTPUT_DIR / "individuales" / "md"
    bundle_out_dir = OUTPUT_DIR / "bundles" / "md"
    
    # Aseguramos forzosamente que la carpeta de destino exista
    bundle_out_dir.mkdir(parents=True, exist_ok=True)
    
    md_files = list(md_in_dir.glob("*.md"))
    
    if not md_files:
        console.print("[yellow]No hay archivos Markdown en la carpeta de individuales para empaquetar.[/yellow]")
        return
        
    console.print(f"\n[bold blue]Iniciando evaluación para Bundling...[/bold blue]")
    
    total_size_bytes = 0
    total_chars = 0
    file_stats = []
    
    for f in md_files:
        size = f.stat().st_size
        total_size_bytes += size
        with open(f, "r", encoding="utf-8") as file_obj:
            content = file_obj.read()
            chars = len(content)
            total_chars += chars
            file_stats.append({"name": f.name, "size": size, "chars": chars, "content": content})
            
    total_size_mb = total_size_bytes / (1024 * 1024)
    
    table = Table(title="Resumen de Archivos Disponibles")
    table.add_column("Archivo", style="cyan")
    table.add_column("Tamaño (KB)", justify="right", style="magenta")
    table.add_column("Caracteres", justify="right", style="green")
    
    for stat in file_stats:
        table.add_row(stat["name"], f"{stat['size'] / 1024:.1f}", f"{stat['chars']:,}")
        
    console.print(table)
    console.print(f"\n[bold]Total de archivos:[/bold] {len(md_files)}")
    console.print(f"[bold]Peso total estimado:[/bold] {total_size_mb:.2f} MB")
    console.print(f"[bold]Caracteres totales:[/bold] {total_chars:,}")
    
    sugerencia = 1
    if total_size_mb > 45 or total_chars > 500000:
        sugerencia = max(2, int(total_size_mb // 45) + 1)
        console.print(f"[yellow]⚠️ El volumen es alto. Sugerimos dividir en al menos {sugerencia} archivos.[/yellow]")
    else:
        console.print("[green]✔ El volumen es manejable para un solo archivo bundle.[/green]\n")

    # FIX: Usamos typer.prompt que no falla en terminales de VS Code
    num_bundles = typer.prompt("¿En cuántos archivos (bundles) deseas dividir este contenido?", default=sugerencia, type=int)
    
    if num_bundles < 1:
        console.print("[red]El número debe ser al menos 1.[/red]")
        return

    _distribute_and_write_bundles(file_stats, num_bundles, bundle_out_dir)

def _distribute_and_write_bundles(file_stats: list, num_bundles: int, out_dir: Path):
    chunk_size = len(file_stats) // num_bundles
    remainder = len(file_stats) % num_bundles
    
    bundles = []
    start = 0
    for i in range(num_bundles):
        end = start + chunk_size + (1 if i < remainder else 0)
        bundles.append(file_stats[start:end])
        start = end
        
    console.print(f"\n[bold blue]Generando {num_bundles} bundle(s)...[/bold blue]")
    
    for i, bundle in enumerate(bundles):
        if not bundle:
            continue
            
        bundle_num = i + 1
        bundle_name = f"bundle_contexto_parte_{bundle_num:02d}.md"
        bundle_path = out_dir / bundle_name
        
        final_content = f"# CONTEXTO DOCUMENTAL - PARTE {bundle_num} de {num_bundles}\n\n"
        final_content += "## 📑 ÍNDICE DE ARCHIVOS INCLUIDOS EN ESTE BUNDLE\n"
        final_content += "> *Este documento es una consolidación de múltiples fuentes. A continuación se listan los archivos originales contenidos aquí:*\n\n"
        
        for file_data in bundle:
            final_content += f"- **{file_data['name']}** ({file_data['chars']:,} caracteres)\n"
            
        final_content += "\n---\n\n"
        
        for file_data in bundle:
            final_content += f"\n\n========================================================================\n"
            final_content += f"📄 INICIO DE DOCUMENTO: {file_data['name']}\n"
            final_content += f"========================================================================\n\n"
            final_content += file_data["content"]
            final_content += f"\n\n[FIN DEL DOCUMENTO: {file_data['name']}]\n"
            
        with open(bundle_path, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        console.print(f"  [green]✔ {bundle_name} creado exitosamente con {len(bundle)} archivos.[/green]")
        
    console.print("\n[bold green]¡Empaquetado finalizado listo para subir al GPT![/bold green]")