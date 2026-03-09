# Documentación de Fase: 2. Motor de Ingesta y Clasificación

**Propósito de la Fase:** Aislar los archivos originales (inputs manuales) del entorno de procesamiento. El objetivo es descubrir los documentos en las carpetas de ingesta, validarlos, calcular firmas criptográficas (hashes MD5) y moverlos a un entorno intermedio seguro (`staging`) para su extracción estructurada.

**Archivos Creados/Modificados:**
1. `src/utils/paths.py`: Genera automáticamente la estructura de directorios (idempotencia de rutas).
2. `src/utils/hashing.py`: Lógica de *chunking* para calcular MD5 sin desbordar memoria RAM en archivos masivos.
3. `src/ingest/discover_files.py`: Escanea recursivamente, filtra por extensiones permitidas, renombra archivos con sufijos de hash para evitar colisiones y los copia a `staging/originals_index`.
4. `main.py`: Se conectó el comando `ingest` de la CLI a la lógica de descubrimiento.

**Estrategia Aplicada:**
- **Inmutabilidad y Trazabilidad:** Los archivos originales en `data/ingest/` nunca se modifican. Se copian a `staging` asegurando que el pipeline analítico no destruya la fuente.
- **Idempotencia:** Al inyectar los primeros 8 caracteres del hash MD5 al nombre en *staging*, el sistema detecta si un archivo ya fue procesado y evita redundancias costosas.
- **Auditoría (Manifiesto):** Se genera `latest_ingest_manifest.json` que contiene el mapeo exacto de dónde viene el archivo y cómo se llama ahora en el sistema interno, preparando el terreno para la trazabilidad final que leerá el Agente GPT.

**Resultado Esperado:**
Al ejecutar `python main.py ingest --all` (habiendo colocado un PDF o Excel de prueba dentro de `data/ingest/inbox/`), el sistema creará todas las carpetas necesarias, calculará el hash, copiará el archivo a `data/staging/originals_index/` y generará un log JSON del proceso en consola.