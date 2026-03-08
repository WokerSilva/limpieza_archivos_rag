import pandas as pd
from pathlib import Path
from rich.console import Console

console = Console()

def process_spreadsheet(file_path: Path, max_rows_md: int = 500) -> dict:
    """
    Procesa archivos Excel y CSV de forma robusta.
    Devuelve un diccionario con el contenido Markdown (resumen o tabla completa) 
    y la estructura JSON completa para el agente.
    """
    console.print(f"    [dim]Iniciando motor Pandas para datos tabulares...[/dim]")
    
    ext = file_path.suffix.lower()
    results = {"markdown": "", "json_data": {}}
    
    try:
        if ext == ".csv":
            # Leer CSV (asumimos UTF-8 por defecto)
            df = pd.read_csv(file_path)
            sheet_data = _process_dataframe(df, "CSV_Data", max_rows_md)
            results["markdown"] += f"## Archivo CSV\n\n{sheet_data['markdown']}\n\n"
            results["json_data"]["CSV_Data"] = sheet_data["json"]
            
        elif ext == ".xlsx":
            # Leer Excel soportando múltiples hojas
            xls = pd.ExcelFile(file_path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                sheet_data = _process_dataframe(df, sheet_name, max_rows_md)
                
                results["markdown"] += f"## Hoja: {sheet_name}\n\n"
                results["markdown"] += sheet_data["markdown"] + "\n\n"
                results["json_data"][sheet_name] = sheet_data["json"]
                
        return results
        
    except Exception as e:
        console.print(f"    [bold red]Error procesando la hoja de cálculo {file_path.name}: {str(e)}[/bold red]")
        raise e

def _process_dataframe(df: pd.DataFrame, name: str, max_rows: int) -> dict:
    """Procesa un DataFrame individual: limpia NaNs y decide la estrategia MD/JSON."""
    # Limpieza básica: quitar columnas/filas completamente vacías
    df = df.dropna(how='all').dropna(axis=1, how='all')
    # Rellenar nulos con string vacío para evitar que el JSON se rompa con valores NaN
    df = df.fillna("") 
    
    num_rows, num_cols = df.shape
    
    # 1. Generar JSON (Lista de diccionarios / JSON-records)
    json_records = df.to_dict(orient="records")
    
    # 2. Generar Markdown inteligente
    if num_rows <= max_rows:
        # Si es manejable, pasamos todo a Markdown
        md_table = df.to_markdown(index=False)
        md_content = f"**Dimensiones:** {num_rows} filas x {num_cols} columnas.\n\n{md_table}"
    else:
        # Si es masiva, hacemos un resumen ejecutivo + muestra
        md_table = df.head(10).to_markdown(index=False)
        md_content = (
            f"**⚠️ Hoja Masiva Detectada:** {num_rows} filas x {num_cols} columnas.\n\n"
            f"> *Nota para el Agente GPT: Esta tabla excede el límite de filas recomendado para visualización directa. "
            f"Solo se muestran las primeras 10 filas como muestra estructural de las columnas. "
            f"Para realizar búsquedas, cruces o análisis determinista fila por fila, debes consultar el archivo `.json` asociado a este documento.*\n\n"
            f"**Muestra de datos (Top 10):**\n\n{md_table}"
        )
        
    return {"markdown": md_content, "json": json_records}