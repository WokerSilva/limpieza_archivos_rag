# Documentación de Fase: 5. Flujo de Bundling (Empaquetado Interactivo)

**Propósito de la Fase:** Solucionar el límite de archivos adjuntos y de tokens en los Agentes GPT. Se consolida el conocimiento generado en las fases anteriores (archivos `.md` individuales) en contenedores o "Bundles" optimizados, inyectando índices y separadores claros para que el LLM no pierda la estructura ni el contexto al analizar grandes volúmenes de texto.

**Archivos Creados/Modificados:**
1. `src/bundle/builder.py`: Motor matemático e interactivo. Calcula en tiempo real el peso (MB) y los caracteres de los archivos procesados. Utiliza `rich.prompt` para detener la ejecución y preguntar al ingeniero cómo desea particionar la información.
2. `main.py`: Se conectó el comando `bundle` a la CLI principal.

**Estrategia Aplicada (Inyección de Contexto RAG):**
- **Árbol de Directorio:** Al inicio de cada `bundle_X.md`, el sistema inyecta un índice dinámico. Esto es un "hack" de Prompt Engineering pasivo que le dice al GPT exactamente qué archivos contiene ese bloque de texto.
- **Limitación Preventiva:** Si el peso supera los 45MB o los 500,000 caracteres, el sistema detecta el riesgo de saturación de ventana de contexto y sugiere proactivamente en cuántos archivos se debería dividir el lote.

**Resultado Esperado:**
Al ejecutar `python main.py bundle`, la terminal mostrará una tabla elegante con los archivos listos, el peso total y pedirá confirmación numérica. Al ingresar la cantidad, generará archivos como `bundle_contexto_parte_01.md` en `data/output/bundles/md/`, listos para arrastrar y soltar en la interfaz del GPT.