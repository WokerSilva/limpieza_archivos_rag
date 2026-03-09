# Documentación de Fase: 3. Core de Extracción y Normalización (PDF/DOCX)

**Propósito de la Fase:** Transformar los documentos aislados en la carpeta de `staging` (PDFs) a un formato semánticamente estructurado (`Markdown`), priorizando la velocidad, la eficiencia de memoria y la compatibilidad estricta con entornos corporativos (offline y detrás de firewalls).

**Archivos Creados/Modificados:**
1. `src/extractors/doc_extractor.py`: Módulo de conexión con `PyMuPDF4LLM`. Se encarga de leer el binario del PDF y exportar el contenido, detectando párrafos y tablas, directo a sintaxis Markdown.
2. `src/flows/process_folder.py`: Orquestador de flujo actualizado. Enruta los PDFs al motor de extracción, inyecta metadatos de trazabilidad (Frontmatter) y guarda el resultado en `output/individuales/md/`.
3. `requirements.txt`: Se añadió `pymupdf4llm` como dependencia principal para esta capa.

**Estrategia Aplicada (Pivote Arquitectónico):**
- **Deuda Técnica y Bloqueos Corporativos:** Se descartó el uso inicial de motores basados en Deep Learning (como Docling/RapidOCR) debido a su alto consumo de RAM (causando errores `std::bad_alloc` en documentos con imágenes pesadas) y su dependencia de descargas dinámicas desde Hugging Face, lo cual es inviable en redes corporativas aseguradas.
- **Eficiencia y Naturaleza Offline:** Se implementó `PyMuPDF4LLM` como motor principal. Esto garantiza que el pipeline de limpieza pueda ejecutarse en cualquier hardware (incluso sin GPU) y sin requerir permisos de Administrador o conexión a internet durante el procesamiento.
- **Inyección de Trazabilidad:** Al inicio de cada archivo `.md` generado, se inyecta un bloque indicando el nombre original y el hash. Cuando los archivos se unan en el futuro, el Agente sabrá exactamente de dónde proviene cada fragmento de información.

**Resultado Esperado:**
Al ejecutar `python main.py process`, el sistema lee el manifiesto, activa el extractor ligero, procesa el documento en segundos y crea un archivo `.md` estructurado en `data/output/individuales/md/`.