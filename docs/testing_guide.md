# Guía de Pruebas Unitarias (Testing Guide)

**Propósito:** Este documento detalla la estrategia de pruebas automatizadas del proyecto `limpieza_archivos_rag`. Utilizamos `pytest` para garantizar la estabilidad del código base y evitar regresiones cuando se integran nuevas funcionalidades.

## 1. Ejecución de Pruebas

Para ejecutar la batería completa de pruebas, asegúrate de tener tu entorno virtual activado y ejecuta en la raíz del proyecto:

```bash
pytest

```

**Opciones útiles:**

* `pytest -v`: Ejecuta las pruebas en modo "verbose" (detallado), mostrando el nombre de cada prueba que pasa o falla.
* `pytest tests/test_ingest.py`: Ejecuta únicamente las pruebas de un archivo específico.

## 2. Estructura de las Pruebas

Las pruebas se encuentran en el directorio `tests/` y siguen el principio AAA (Arrange, Act, Assert):

1. **Arrange (Preparar):** Configurar los datos falsos o archivos temporales necesarios.
2. **Act (Actuar):** Ejecutar la función específica del pipeline (ej. `calculate_file_hash`).
3. **Assert (Afirmar):** Comprobar que el resultado devuelto por la función coincide matemáticamente o lógicamente con el resultado esperado.

## 3. Cobertura Actual

* **`test_utils.py`:** Garantiza la inmutabilidad de la lectura criptográfica por chunks (Hash MD5).
* **`test_ingest.py`:** Protege el pipeline contra caídas en motores C++ (como el usado por PyMuPDF) verificando que el sanitizador de nombres de archivo siempre elimine acentos y caracteres prohibidos.

## 4. Cómo agregar nuevas pruebas

Al construir nuevos extractores (ej. un OCR avanzado en el futuro), se debe crear un archivo `test_[modulo].py` dentro de la carpeta `tests/`. Las funciones de prueba deben comenzar con el prefijo `test_` para que el motor las descubra automáticamente.

```

---

### 🚀 ¡Hora de Correr el Test!

Abre tu terminal (asegúrate de que el entorno virtual siga activo) y escribe simplemente:

```bash
pytest -v

```