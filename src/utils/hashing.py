import hashlib
from pathlib import Path

def calculate_file_hash(file_path: Path, chunk_size: int = 8192) -> str:
    """Calcula el hash MD5 de un archivo leyendo en fragmentos."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()