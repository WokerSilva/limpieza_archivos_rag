import tempfile
import os
from pathlib import Path
from src.utils.hashing import calculate_file_hash

def test_calculate_file_hash():
    """
    Verifica que la función de hashing MD5 lea correctamente en fragmentos
    y devuelva una cadena hexadecimal de 32 caracteres consistente.
    """
    # 1. Preparación (Arrange): Creamos el archivo y forzamos su cierre para liberar el buffer
    tmp_fd, tmp_path_str = tempfile.mkstemp()
    tmp_path = Path(tmp_path_str)
    
    try:
        # Escribimos los bytes y cerramos el file descriptor explícitamente
        with os.fdopen(tmp_fd, 'wb') as f:
            f.write(b"Hello RAG Pipeline")

        # 2. Acción (Act): Calculamos el hash
        hash_val = calculate_file_hash(tmp_path)
        
        # 3. Verificación (Assert): 
        assert len(hash_val) == 32  # El MD5 siempre debe tener 32 caracteres
        assert hash_val == "af6f349e840fa72486d510f4ad62eeb0" # Hash MD5 real de "Hello RAG Pipeline"
        
    finally:
        # Limpiamos el archivo temporal del sistema
        if tmp_path.exists():
            tmp_path.unlink()