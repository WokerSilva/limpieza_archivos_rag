from pathlib import Path

# Raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# Carpetas principales
INGEST_DIR = DATA_DIR / "ingest"
STAGING_DIR = DATA_DIR / "staging"
OUTPUT_DIR = DATA_DIR / "output"
CACHE_DIR = DATA_DIR / "cache"
LOGS_DIR = DATA_DIR / "logs"

def ensure_directories():
    """Crea la estructura de directorios base si no existe."""
    directories_to_create = [
        INGEST_DIR / "inbox",
        INGEST_DIR / "lotes",
        STAGING_DIR / "originals_index",
        STAGING_DIR / "temp",
        OUTPUT_DIR / "individuales" / "md",
        OUTPUT_DIR / "individuales" / "json",
        OUTPUT_DIR / "bundles" / "md",
        CACHE_DIR / "hashes",
        LOGS_DIR / "audit"
    ]
    
    for dir_path in directories_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)