# Documentación de Fase: 4. Core de Datos Tabulares (Excel/CSV)

**Propósito de la Fase:** Procesar hojas de cálculo y bases de datos tabulares resolviendo el problema crítico de la "explosión de tokens" en los modelos LLM. Se implementa una estrategia dual donde el contenido tabular se evalúa por su peso y dimensiones, generando representaciones amigables para la lectura visual (Markdown) y para la consulta estructurada fila por fila (JSON).

**Archivos Creados/Modificados:**
1. `src/extractors/spreadsheet.py`: Nuevo motor basado en `pandas` y `openpyxl`. Limpia filas/columnas vacías y aplica lógica condicional. Extrae múltiples hojas de un mismo `.xlsx`.
2. `src/flows/process_folder.py`: Se actualizó el orquestador para capturar la extensión `.xlsx` y `.csv`, y exportar simultáneamente los resultados a `output/individuales/md/` y `output/individuales/json/`.

**Estrategia Aplicada (Salida Dual Inteligente):**
- **Umbral de Filas:** Si la hoja tiene menos de 500 filas, se renderiza completamente como una tabla en Markdown (para asimilación visual rápida). 
- **Modo Masivo:** Si la hoja excede el umbral, el Markdown generado funciona como un "Resumen Ejecutivo", mostrando solo las dimensiones y las primeras 10 filas, junto con una advertencia (Prompt Inyectado) que instruye al Agente GPT a utilizar el archivo JSON correspondiente para cruces de datos o consultas deterministas, evitando que el modelo alucine o sature su ventana de contexto.

**Resultado Esperado:**
Al ingresar un archivo `.xlsx` (incluso con múltiples hojas) en `ingest/xlsx/`, el comando `python main.py process` generará un archivo `.md` (con el frontmatter y las tablas/resúmenes) y un archivo `.json` idéntico en nombre, que contiene la data estructurada en un formato `records` (lista de diccionarios) ideal para analítica de datos por IA.