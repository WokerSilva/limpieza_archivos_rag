# Roadmap Estratégico y Plan de Mejoras (V2+)

**Documento de Evolución del Sistema ETL Documental**

## 🎯 Visión a Futuro

La Versión 1.0 ha resuelto la extracción offline, el control de tokens y la partición dual de datos tabulares. El objetivo de las siguientes iteraciones es dotar al sistema de capacidades de visión (OCR local), fragmentación semántica avanzada y preparación para integrarse directamente con arquitecturas multi-agente de previsión estratégica e inteligencia de negocios.

## 🚀 Horizonte 1: Mejoras a Corto Plazo (V1.5)

*Enfocadas en robustecer la extracción y el control de calidad.*

* **Módulo de OCR de Respaldo (`src/ocr/`):**
* **Problema:** PyMuPDF ignora el texto incrustado en imágenes dentro de PDFs escaneados.
* **Solución:** Integrar `pytesseract` o `OCRmyPDF` como un paso opcional (`--use-ocr`). Si PyMuPDF detecta que una página tiene menos de 50 caracteres de texto seleccionable, el orquestador activará el OCR local automáticamente para recuperar esa información antes de pasar a Markdown.


* **Soporte Nativo Ampliado (DOCX y PPTX):**
* **Mejora:** Implementar `mammoth` o `python-docx` en el extractor de Word para capturar metadatos semánticos más puros (Heading 1, Heading 2), y habilitar la conversión de `.pptx` directo a `.md` sin necesidad de guardarlo como PDF previamente.


* **Batería de Pruebas Unitarias (`tests/`):**
* **Mejora:** Usar `pytest` para automatizar la validación de las funciones críticas (ej. asegurar que el cálculo de Hashes MD5 siempre devuelva 32 caracteres y que Pandas no rompa con archivos CSV corruptos).



## 🧠 Horizonte 2: Arquitectura y Semántica (V2.0)

*Enfocadas en mejorar la digestión de la información para los LLMs.*

* **Chunking Semántico (`src/normalize/`):**
* **Problema:** Actualmente el bundling une archivos enteros. Si un archivo tiene 80,000 caracteres, podría ser demasiado denso para búsquedas precisas.
* **Solución:** Implementar divisores de texto (*Text Splitters* tipo LangChain) para cortar los Markdowns respetando los encabezados (ej. nunca cortar a mitad de un párrafo o tabla).


* **Gestor de Assets Visuales (`data/output/individuales/assets/`):**
* **Mejora:** Modificar el extractor para que guarde las gráficas e imágenes importantes del PDF como `.png` en la carpeta de *assets*, e inyecte la ruta local en el Markdown `![Gráfica de Ventas](assets/img_01.png)`. Esto preparará el contexto para modelos multimodales (GPT-4o, Gemini 1.5 Pro).



## 🌐 Horizonte 3: Integración Multi-Agente y Despliegue (V3.0)

*Enfocadas en automatización corporativa y bases de datos vectoriales.*

* **Microservicio Corporativo (API Rest):**
* **Mejora:** Envolver este pipeline CLI en una API local usando **FastAPI**. Esto permitirá que otros sistemas, tableros de Business Intelligence, o agentes de evaluación de proyectos envíen un archivo por POST y reciban el Markdown/JSON estructurado en segundos.


* **Exportación Directa a Vector DB:**
* **Mejora:** En lugar de generar archivos `.md` para subir manualmente a un GPT, el comando `bundle` podría tener un *flag* `--to-vector` que convierta los chunks de texto en Embeddings locales (usando modelos de HuggingFace offline) y los guarde en una base de datos vectorial como **ChromaDB** o **FAISS**, creando el motor de recuperación (RAG) completo 100% en local.