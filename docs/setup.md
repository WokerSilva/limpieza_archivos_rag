# Guía de Configuración y Referencia Técnica (Setup)

**Estado del Documento:** Versión 1.0 (Completada)  
**Propósito:** Proveer instrucciones claras para levantar el entorno de desarrollo, documentar las dependencias clave, listar los comandos disponibles y explicar el flujo de trabajo interno del sistema de limpieza de archivos RAG.

---

## 1. Configuración del Entorno (Setup Local)

Este proyecto está diseñado para ejecutarse 100% de forma local, asegurando la privacidad de los datos y la compatibilidad con redes corporativas (sin llamadas externas a APIs).

### Pasos de Instalación:
1. **Crear el entorno virtual:**
   ```bash
   python -m venv venv

```

2. **Activar el entorno virtual:**
* En Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
* En Linux/Mac: `source venv/bin/activate`


3. **Instalar dependencias:**
```bash
pip install -r requirements.txt

```



---

## 2. Dependencias y Paquetes Clave

El sistema se apoya en librerías open-source altamente optimizadas:

* **`typer` & `rich`:** Construyen la Interfaz de Línea de Comandos (CLI) interactiva.
* **`pymupdf4llm`:** Motor principal de extracción para PDFs. Es **100% offline**, consume muy poca memoria RAM (evita colapsos) y exporta tablas/layouts a Markdown a gran velocidad, ideal para firewalls corporativos.
* **`pandas` & `openpyxl`:** Motores para el procesamiento dual de datos tabulares, capaces de sanitizar nulos, manejar fechas complejas y exportar simultáneamente a Markdown (resúmenes) y JSONL (datos estructurados).

---

## 3. Comandos Disponibles (CLI)

El punto de entrada de la aplicación es `main.py`.

* **`python main.py ingest --all`**
* **Qué hace:** Escanea la carpeta `data/ingest/` (y subcarpetas). Sanitiza los nombres (quita acentos/espacios), calcula hashes MD5 y copia los originales a `staging/originals_index/` generando un manifiesto de trazabilidad.


* **`python main.py process`**
* **Qué hace:** Lee el manifiesto y extrae la información.
* Si es **PDF/DOCX**: Llama a PyMuPDF y genera un `.md` estructurado.
* Si es **XLSX/CSV**: Genera un `.md` para lectura visual y un `.json` seguro (serializando fechas y nulos) para análisis de datos puro.




* **`python main.py bundle`**
* **Qué hace:** Evalúa el peso y la cantidad de caracteres de los archivos `.md` resultantes. Muestra una tabla interactiva en consola y empaqueta los archivos inyectando un índice RAG para evitar saturar el contexto de los LLMs.



---

## 4. Arquitectura de Directorios

El flujo respeta una arquitectura ETL clásica de ingeniería de datos:

* `data/ingest/`: Entrada manual y desordenada del usuario.
* `data/staging/`: Entorno seguro, inmutable y cacheado (hashes MD5).
* `data/output/individuales/`: Archivos RAG 1-a-1 en `.md` y `.json`.
* `data/output/bundles/`: Consolidaciones listas para subir al Agente GPT.

---

## 5. Directorio de Módulos Centrales (`src/`)

* **`main.py`:** Enrutador de comandos CLI.
* **`src/utils/paths.py` & `hashing.py`:** Utilidades del sistema (rutas dinámicas, MD5 por chunks).
* **`src/ingest/discover_files.py`:** Limpieza de nombres, control de redundancias y logs JSON.
* **`src/flows/process_folder.py`:** El orquestador; decide qué extractor usar.
* **`src/extractors/doc_extractor.py`:** Wrapper offline para PDFs (`pymupdf4llm`).
* **`src/extractors/spreadsheet.py`:** Wrapper de datos tabulares (estrategia dual `pandas`).
* **`src/bundle/builder.py`:** Motor matemático e interactivo para empaquetado seguro.