from src.ingest.discover_files import sanitize_filename

def test_sanitize_filename_accents_and_spaces():
    """Verifica que los acentos y espacios se eliminen o reemplacen correctamente."""
    raw_name = "Titulación Proyecto"
    clean_name = sanitize_filename(raw_name)
    assert clean_name == "Titulacion_Proyecto"

def test_sanitize_filename_special_characters():
    """Verifica que los caracteres especiales problemáticos se conviertan en guiones bajos."""
    raw_name = "Reporte#Financiero!2026@Ventas"
    clean_name = sanitize_filename(raw_name)
    assert clean_name == "Reporte_Financiero_2026_Ventas"

def test_sanitize_filename_safe_string():
    """Verifica que un nombre que ya es seguro no sufra modificaciones inesperadas."""
    raw_name = "archivo_seguro-v1.0"
    clean_name = sanitize_filename(raw_name)
    assert clean_name == "archivo_seguro-v1.0"