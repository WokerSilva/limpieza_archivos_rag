# Documentación de Fase: 1. Configuración Base y Esqueleto CLI

**Propósito de la Fase:** Establecer los cimientos del proyecto. Esto incluye la gestión de dependencias, variables de entorno, configuraciones de negocio centralizadas y la estructura principal de la interfaz de línea de comandos (CLI) que orquestará todo el flujo ETL.

**Archivos Creados/Modificados:**
1. `requirements.txt`: Define el stack tecnológico (Typer, Docling, Pandas, etc.).
2. `.env.example`: Protege las rutas locales y configuraciones dependientes del SO.
3. `config/settings.yaml`: Desacopla las "reglas duras" (límites de MB, umbrales de Excel) del código Python.
4. `main.py`: Punto de entrada de Typer con los comandos `ingest`, `process` y `bundle` mapeados.

**Estrategia Aplicada:**
- **Modularidad temprana:** Al separar `settings.yaml` y `.env`, el código Python no tendrá valores quemados, permitiendo escalar a servidores distintos o ajustar límites para diferentes GPTs sin tocar la lógica.
- **CLI Amigable:** Se integró `Rich` con `Typer` para asegurar que los logs y advertencias en terminal sean legibles y claros para el operador humano que ejecutará el *bundling* manual.

**Resultado Esperado:**
Un entorno virtual funcional. El desarrollador puede ejecutar `pip install -r requirements.txt` y correr `python main.py --help` para ver la estructura de comandos lista para ser integrada con la lógica de negocio en la siguiente fase.