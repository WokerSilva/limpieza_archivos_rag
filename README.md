# Documento Base del Proyecto  
## Sistema local de limpieza, extracción estructurada y empaquetado documental para consumo por LLMs

**Versión:** 0.1  
**Estado:** Documento inicial de alineación  
**Propósito:** Definir el objetivo, alcance, estrategia técnica y solución propuesta para el proyecto de limpieza y transformación de archivos hacia salidas estructuradas en Markdown y JSON, listas para ser utilizadas por agentes GPT en un entorno local y seguro.

---

## 1. Contexto general

Este proyecto nace de una necesidad concreta: **procesar documentos heterogéneos de forma local, segura y robusta**, para convertirlos en una representación textual estructurada que pueda ser consumida de forma más eficiente por modelos GPT.

La motivación principal es evitar depender del archivo original como entrada directa del modelo. En su lugar, se busca construir un flujo donde los documentos se:

1. reciben,
2. clasifican,
3. extraen,
4. limpian,
5. estructuran,
6. convierten a Markdown y/o JSON,
7. y posteriormente se pueden unir en uno o varios archivos finales optimizados para su uso dentro de un GPT.

Esto permite trabajar con archivos de distintos tipos bajo una lógica común, mejorar la legibilidad para el modelo, aumentar la trazabilidad del contenido y mantener todo el procesamiento **100% local**, sin exponer información sensible a servicios externos.

---

## 2. Objetivo del proyecto

Diseñar e implementar un sistema en **Python**, ejecutado localmente, capaz de:

- procesar distintos tipos de archivos documentales;
- extraer su contenido con la mayor fidelidad posible;
- conservar, reconstruir o aproximar la estructura lógica del documento;
- detectar y tratar componentes relevantes como títulos, tablas, secciones, bloques y contenido OCR;
- generar una salida enriquecida en **Markdown** y, cuando convenga, en **JSON**;
- y crear archivos consolidados listos para ser utilizados como contexto en GPTs o flujos tipo RAG manual.

---

## 3. Tipos de archivo contemplados

En la primera fase del proyecto se consideran los siguientes formatos de entrada:

- **PDF con texto digital**
- **PDF escaneado**
- **PDF proveniente de PowerPoint**
- **DOCX**
- **XLSX**
- **CSV**

### Consideraciones importantes
- Los PowerPoint se tratarán **en su representación PDF**, no como `.pptx` en esta primera etapa.
- Los Excel y CSV tendrán un tratamiento especial, porque su representación óptima para LLM no siempre será Markdown puro.
- Los PDFs pueden contener:
  - imágenes incrustadas,
  - tablas complejas,
  - múltiples columnas,
  - encabezados y pies repetidos,
  - notas al pie,
  - anexos,
  - y páginas escaneadas.

---

## 4. Alcance funcional

El sistema debe cubrir dos grandes flujos:

### Flujo 1: procesamiento individual
Convierte un archivo o un conjunto de archivos originales en salidas estructuradas por documento.

**Entrada:**
- un archivo individual,
- una carpeta por tipo,
- o una subcarpeta/lote manual.

**Salida esperada por archivo:**
- un archivo `.md` principal;
- opcionalmente un `.json` complementario;
- assets asociados si aplica;
- reporte de procesamiento.

### Flujo 2: unión y empaquetado
Permite seleccionar manualmente varios archivos ya procesados y unirlos en uno o varios Markdown finales optimizados para cargarse en GPT.

**Objetivo del flujo 2:**
- conservar trazabilidad de origen;
- añadir índice o árbol inicial;
- controlar tamaño final del archivo;
- sugerir cuántos bundles generar;
- evitar saturación al momento de usarlos en GPT.

---

## 5. Principios de diseño del sistema

Este proyecto se construye sobre los siguientes principios:

### 5.1 Privacidad total
Toda la información debe procesarse **de manera local**.  
No se deben usar APIs externas, servicios cloud ni soluciones que impliquen salida de datos a terceros.

### 5.2 Robustez antes que improvisación
La solución debe apoyarse en librerías y prácticas ya probadas, evitando una arquitectura basada en prueba y error sin criterio.

### 5.3 Representación estructurada antes que texto plano
No conviene extraer únicamente texto crudo.  
La mejor estrategia es trabajar con una representación intermedia estructurada del documento y a partir de ella derivar:
- Markdown para lectura por GPT,
- JSON para estructuras tabulares o análisis fila a fila.

### 5.4 Trazabilidad
Todo fragmento relevante debe poder relacionarse con:
- archivo de origen,
- página, hoja o bloque,
- método de extracción,
- advertencias de calidad.

### 5.5 Modularidad
Cada fase del pipeline debe estar separada:
- ingesta,
- OCR,
- extracción,
- normalización,
- renderizado,
- unión final.

---

## 6. Estrategia técnica propuesta

La estrategia técnica general aprobada para esta fase es la siguiente:

### 6.1 Arquitectura por capas
El sistema se organiza en capas claras:

1. **Ingesta**
2. **Staging**
3. **Extracción**
4. **OCR**
5. **Normalización**
6. **Renderizado**
7. **Bundling / unión**
8. **Salida**
9. **Logs / auditoría / cache**

### 6.2 Modelo canónico interno
Antes de escribir Markdown o JSON, el sistema debe construir una forma interna homogénea del documento.

Ese modelo canónico debe representar, al menos:
- metadatos del documento;
- páginas u hojas;
- párrafos;
- títulos;
- tablas;
- imágenes o referencias visuales;
- advertencias;
- origen de la extracción.

Este punto es clave porque evita depender del formato nativo de cada librería y permite:
- cambiar extractores sin romper el resto del sistema;
- generar múltiples tipos de salida;
- aplicar limpieza y transformación de forma consistente.

### 6.3 Motores y enfoque recomendado
La arquitectura técnica validada para esta primera etapa se basa en:

- **Docling** como motor principal de parsing multi-formato;
- **OCRmyPDF + Tesseract** para PDFs escaneados;
- **PyMuPDF / PyMuPDF4LLM** como apoyo y fallback para PDFs difíciles;
- **pandas + openpyxl** para XLSX/CSV;
- **python-docx** como apoyo para inspección o fallback en DOCX;
- **Typer** para la CLI del proyecto.

---

## 7. Solución propuesta por tipo de archivo

### 7.1 PDF con texto digital
Ruta principal:
- parsear el documento,
- extraer bloques, secciones y tablas,
- reconstruir orden de lectura,
- limpiar duplicados de encabezados/pies.

**Salida:**
- Markdown estructurado;
- JSON auxiliar si se detectan tablas relevantes o metadatos útiles.

### 7.2 PDF escaneado
Ruta propuesta:
1. detectar ausencia o baja calidad de capa textual;
2. ejecutar OCR local;
3. reinyectar texto al pipeline documental;
4. normalizar estructura resultante.

**Advertencia:**  
El OCR puede no recuperar perfectamente el layout original.  
Por ello, el sistema debe distinguir entre contenido:
- extraído nativamente,
- y contenido recuperado por OCR.

### 7.3 PDF proveniente de PowerPoint
Tratamiento como PDF estructurado.  
Se debe intentar recuperar:
- títulos de diapositiva,
- bullets,
- bloques,
- tablas,
- texto dentro de imágenes si existe OCR posible.

### 7.4 DOCX
El documento debe analizarse buscando:
- encabezados,
- subtítulos,
- párrafos,
- tablas,
- listas,
- imágenes o referencias embebidas.

La salida esperada será Markdown estructurado, más JSON complementario si las tablas lo requieren.

### 7.5 XLSX / CSV
Este tipo de archivo tendrá una estrategia especial.

#### Principio clave
Para hojas largas, **no es recomendable usar únicamente Markdown** como forma principal, porque:
- crece mucho en tamaño,
- pierde eficiencia para el modelo,
- y complica el análisis fila a fila.

#### Estrategia recomendada
- generar una vista Markdown resumida y legible;
- generar un JSON o JSONL por hoja o por partición;
- preservar nombres de columnas;
- permitir revisión fila a fila por parte del agente.

#### Casos a contemplar
- múltiples hojas;
- celdas combinadas;
- encabezados multinivel;
- datos largos;
- estructura no uniforme.

---

## 8. Manejo de imágenes y contenido visual

El proyecto no debe ignorar por completo las imágenes.  
Sin embargo, su tratamiento debe ser progresivo y controlado.

### Niveles propuestos
**Nivel 1:** extraer texto visible vía OCR si existe.  
**Nivel 2:** si no se puede interpretar completamente, dejar marcador estructurado en Markdown.  
**Nivel 3:** opcionalmente exportar el asset y referenciarlo.  
**Nivel 4:** una fase futura podría incluir descripción local de imágenes, siempre sin nube.

### Regla operativa
Aunque una imagen no pueda interpretarse bien, **el texto principal del documento debe salir completo o lo más completo posible**.

---

## 9. Estrategia de salida

### 9.1 Salida individual
Cada archivo procesado debe generar, como mínimo:

- `archivo_original.md`
- `archivo_original.report.json`

Y opcionalmente:
- `archivo_original.json`
- carpeta `archivo_original.assets/`

### 9.2 Salida consolidada
El flujo de bundling debe generar:

- `bundle_01.md`
- `bundle_02.md`
- `bundle_manifest.json`

### 9.3 Estructura interna del Markdown
Cada Markdown final debe incluir:
- título o encabezado del documento;
- trazabilidad mínima;
- bloques bien separados;
- tablas cuando sea posible;
- secciones claramente delimitadas;
- marcadores cuando exista contenido visual no completamente interpretado.

---

## 10. Estrategia del flujo de unión

La unión de archivos no será automática sin criterio.  
Debe ser una **acción manual asistida por terminal**.

### Objetivos del flujo de unión
- permitir al usuario elegir qué documentos unir;
- calcular peso y tamaño;
- sugerir número de bundles;
- conservar índice inicial;
- mantener trazabilidad de origen;
- optimizar archivos finales para su uso dentro de GPT.

### Criterios de evaluación
Este flujo deberá considerar al menos:
- tamaño del archivo final;
- longitud total aproximada;
- posible saturación de contexto operativo.

### Regla operativa
El sistema debe poder sugerir:
- un solo bundle si conviene;
- dos o más bundles si el contenido es demasiado grande.

---

## 11. Aclaraciones clave del proyecto

### 11.1 No es un OCR-only project
Aunque el OCR es importante, este proyecto no se limita a “leer texto de imágenes”.  
Su enfoque es **documental y estructural**.

### 11.2 No es un RAG completo
Este sistema no implementa, por ahora:
- embeddings,
- vector DB,
- retrieval semántico,
- ranking documental.

Su propósito es generar una **base documental limpia y estructurada** que sirva como insumo para GPT o para una etapa RAG posterior.

### 11.3 No todos los documentos podrán preservarse perfectamente
Habrá documentos donde:
- el orden de lectura sea ambiguo,
- la tabla sea compleja,
- la imagen no sea interpretable,
- o el OCR introduzca ruido.

Por ello, el sistema debe degradar con elegancia y dejar rastros claros de advertencias.

### 11.4 Fidelidad y enriquecimiento deben convivir
El proyecto no debe elegir ciegamente entre:
- máxima fidelidad,
- o máxima reinterpretación para LLM.

La meta es un equilibrio:  
**ser fiel al contenido, pero lo suficientemente estructurado como para que un modelo lo entienda mejor**.

---

## 12. Riesgos y advertencias técnicas

### 12.1 PDFs complejos
Los PDFs pueden romper el orden de lectura, especialmente si tienen:
- dos columnas,
- elementos flotantes,
- tablas embebidas,
- pies de página repetidos.

### 12.2 OCR imperfecto
El OCR local puede fallar en:
- escaneos borrosos,
- baja resolución,
- inclinación,
- texto sobre imágenes complejas.

### 12.3 Excel desordenado
No todos los Excel son bases tabulares limpias.  
Puede haber:
- celdas fusionadas,
- encabezados múltiples,
- hojas con formato visual más que analítico.

### 12.4 Sobrecarga del Markdown
Si se vuelca demasiado contenido sin criterio, el Markdown final puede volverse pesado y poco útil para GPT.

### 12.5 Dependencias del sistema
Algunas herramientas locales pueden requerir instalación adicional en el sistema operativo, especialmente motores OCR.

---

## 13. Puntos clave para el equipo

- Todo debe correr localmente.
- El pipeline debe ser modular.
- El Markdown es una salida importante, pero no la única.
- JSON es indispensable en hojas tabulares largas.
- La unión final debe ser consciente del tamaño.
- La trazabilidad no es opcional.
- El sistema debe registrar advertencias y calidad.
- Se debe priorizar una arquitectura escalable y mantenible desde la V1.

---

## 14. Estructura conceptual del flujo

```text
ingesta
  -> validación
  -> clasificación
  -> staging
  -> OCR si aplica
  -> extracción
  -> normalización
  -> render a markdown/json
  -> salida individual
  -> selección manual de md
  -> unión / bundling
  -> salida final para GPT
```

---

## 15. Resultado esperado de esta fase documental

Al cerrar esta primera documentación, el proyecto queda alineado en los siguientes aspectos:

- objetivo general definido;
- alcance funcional delimitado;
- estrategia técnica validada;
- restricciones de privacidad aclaradas;
- solución por tipo de archivo planteada;
- flujo de unión identificado;
- riesgos técnicos reconocidos;
- y arquitectura conceptual suficientemente madura para comenzar la implementación.

---

## 16. Próximos pasos sugeridos

1. convertir esta documentación en README técnico del repositorio;
2. definir la estructura inicial real del proyecto;
3. crear el `requirements.txt` base;
4. construir la CLI inicial con Typer;
5. definir el modelo canónico interno;
6. implementar el flujo 1;
7. implementar el flujo 2;
8. agregar pruebas y reportes de calidad.

---

## 17. Conclusión

Este proyecto busca resolver de forma práctica, segura y robusta un problema muy común en flujos con LLMs: **cómo transformar documentos reales, desordenados y heterogéneos en una entrada textual útil, trazable y estructurada**.

La propuesta técnica elegida evita depender de nube, protege información sensible, reduce fricción manual y sienta bases sólidas para evolucionar después hacia procesos más avanzados, incluyendo automatización documental, sistemas RAG o agentes especializados.

La prioridad en esta fase no es solo “extraer texto”, sino construir un sistema documental confiable que convierta archivos complejos en conocimiento usable.
