import tempfile
from pathlib import Path
from src.utils.hashing import calculate_file_hash

def test_calculate_file_hash():
    """
    Verifica que la función de hashing MD5 lea correctamente en fragmentos
    y devuelva una cadena hexadecimal de 32 caracteres consistente.
    """
    # 1. Preparación (Arrange): Creamos un archivo temporal con texto conocido
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"Hello RAG Pipeline")
        tmp_path = Path(tmp.name)

    try:
        # 2. Acción (Act): Calculamos el hash
        hash_val = calculate_file_hash(tmp_path)
        
        # 3. Verificación (Assert): 
        assert len(hash_val) == 32  # El MD5 siempre debe tener 32 caracteres
        assert hash_val == "8345c083ba8ebf1b8bb1375d04cc6349" # Hash exacto esperado
    finally:
        # Limpiamos el archivo temporal del sistema
        tmp_path.unlink()