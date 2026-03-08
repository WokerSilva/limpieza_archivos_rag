limpieza_archivos_rag/
├── README.md
├── requirements.txt
├── .env.example
├── main.py
│
├── config/
│   ├── settings.yaml             # Configuraciones globales (límites de tokens, umbrales de tamaño)
│   └── formats.yaml              # Reglas específicas por tipo de archivo
│
├── data/                         # [Directorio ignorado en git]
│   ├── ingest/                   # 1. Entrada manual de archivos originales
│   │   ├── inbox/                # Entrada general libre
│   │   ├── pdf_texto/
│   │   ├── pdf_escaneado/
│   │   ├── pdf_ppt/
│   │   ├── docx/
│   │   ├── xlsx/
│   │   ├── csv/
│   │   └── lotes/                # Subcarpetas para ejecución por lote
│   │
│   ├── staging/                  # 2. Archivos intermedios del pipeline (Idempotencia)
│   │   ├── originals_index/
│   │   ├── ocr/
│   │   ├── extracted_raw/
│   │   ├── normalized/
│   │   └── temp/
│   │
│   ├── output/                   # 3. Salida final del sistema
│   │   ├── individuales/         # Resultados 1 a 1
│   │   │   ├── md/
│   │   │   ├── json/
│   │   │   ├── assets/           # Imágenes extraídas referenciadas
│   │   │   └── reports/
│   │   │
│   │   ├── bundles/              # 4. Unión de varios MD listos para subir al GPT
│   │   │   ├── md/
│   │   │   └── reports/
│   │   │
│   │   └── exports/              # Salidas empaquetadas (zip, manifiestos)
│   │       ├── zip/
│   │       └── manifests/
│   │
│   ├── logs/                     # Auditoría de ejecuciones y errores
│   │   ├── runs/
│   │   ├── errors/
│   │   └── audit/
│   │
│   └── cache/                    # Evita reprocesar archivos no modificados
│       ├── hashes/
│       ├── metadata/
│       └── reused/
│
├── src/                          # Código fuente
│   ├── cli/                      # Comandos de Typer (ingest, process, bundle)
│   ├── core/                     # Modelos de datos (Pydantic), enums, excepciones
│   ├── ingest/                   # Lógica de descubrimiento y validación de inputs
│   ├── extractors/               # Módulos específicos por formato (pdf, docx, etc.)
│   ├── ocr/                      # Integración con Tesseract/OCRmyPDF
│   ├── normalize/                # Limpieza de headers/footers, orden de lectura
│   ├── renderers/                # Generadores de Markdown y JSON
│   ├── bundle/                   # Lógica matemática para unir archivos sin exceder límites
│   ├── flows/                    # Orquestadores de alto nivel (single, folder, batch)
│   └── utils/                    # Funciones auxiliares (hashing, paths, consola)
│
└── tests/                        # Pruebas unitarias y de integración