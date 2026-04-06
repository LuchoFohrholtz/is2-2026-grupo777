## Entrada 001 — Tabla de integrantes y roles del equipo — Semana 1

**Herramienta:** ChatGPT  
**Responsable:** Dev lead

**¿Para qué se usó?**  
Organizar una tabla con los integrantes del equipo, sus roles y sus usuarios de GitHub.  

**¿Qué generó la IA?**  
Una tabla estructurada con columnas de nombre, rol y GitHub, lista para pegar en el documento.  

**¿Qué modificamos y por qué?**  
- Cambiamos nombres de ejemplo por los integrantes reales del equipo.  
- Ajustamos algunos roles para que coincidan con la división de tareas acordada.  
- Revisamos el formato para asegurar compatibilidad con el editor donde se entregaría.  

---

## Entrada 002 — Organización inicial del repositorio GitHub — Semana 1

**Herramienta:** ChatGPT  
**Responsable:** Dev Lead  
**¿Para qué se usó?**  
Definir una estructura ordenada para el repositorio del proyecto y entender cómo dejar GitHub organizado.  

**¿Qué generó la IA?**  
Una propuesta de estructura de carpetas y organización del repositorio, orientada a separar documentación, código fuente y recursos del proyecto.  

**¿Qué modificamos y por qué?**  
- Adaptamos la estructura a las necesidades reales del equipo y de la materia.  
- Quitamos carpetas que todavía no íbamos a usar para no complejizar el repositorio.  
- Conservamos una organización simple para facilitar el trabajo colaborativo.  

---

## Entrada 003 — Gestión de colaboradores en GitHub — Semana 1

**Herramienta:** ChatGPT  
**Responsable:** Scrum Master / Dev Lead  
**¿Para qué se usó?**  
Entender cómo invitar integrantes al repositorio y asignar permisos de edición.  

**¿Qué generó la IA?**  
Instrucciones paso a paso para agregar colaboradores, ubicar la opción correcta en GitHub y verificar permisos de trabajo.  

**¿Qué modificamos y por qué?**  
- No fue necesario modificar contenido técnico, solo adaptar los pasos según la interfaz real que veía el equipo.  
- Se aplicaron los pasos al repositorio concreto del proyecto.  
- Se validó que los miembros puedan editar y participar del tablero.

## Entrada 004 — Estrategias de la Matriz de Riesgos — Semana 2

**Herramienta:** ChatGPT
**Responsable:** Scrum Master / Dev Lead
**¿Para qué se usó?**
Definir estrategias de mitigación preventivas y planes de contingencia reactivos para los 5 riesgos identificados en el borrador del proyecto (Ferretería).

**¿Qué generó la IA?**
Un texto detallado con acciones específicas para cada riesgo, abarcando desde la configuración técnica de la base de datos hasta políticas de commits por problemas de conectividad en la zona.

**¿Qué modificamos y por qué?**
* Ajustamos el vocabulario técnico sugerido por la IA para que coincida con las herramientas reales que usaremos (ej. especificando PostgreSQL/Supabase en lugar de soluciones genéricas).
* Resumimos las políticas de contingencia de equipo para alinearlas con nuestro Contrato de Proyecto y horarios reales de cursada.

---

## Entrada 005 — Generación de Código Mermaid para Diagrama de Clases — Semana 2

**Herramienta:** ChatGPT
**Responsable:** Dev Lead
**¿Para qué se usó?**
Traducir el borrador de entidades lógicas del sistema de inventario (Producto, MovimientoStock, Cliente, Empleado) a sintaxis de código Mermaid para integrarlo visualmente en la documentación.

**¿Qué generó la IA?**
Un bloque de código `classDiagram` y `flowchart LR` con las instancias de objetos, atributos mockeados (ej. Amoladora Caterpillar) y las relaciones de cardinalidad.

**¿Qué modificamos y por qué?**
* Refinamos el diagrama inicial propuesto por la IA (que era un diagrama de clases completo) a un `flowchart LR` más simple para cumplir estrictamente con el nivel de detalle requerido en la protoclase 1.
* Modificamos la entidad genérica "Usuario" sugerida por la IA, separándola en "Empleado" y "Cliente" para reflejar mejor el proceso de venta real en el mostrador. Y luego modificamos los datos colocando ejemplos que sean mas acordes a nuestra ciudad.
* Corregimos un error de sintaxis provocado al intentar renderizar JSON puro dentro del bloque de Mermaid.

## Entrada 006 — División de tareas para el Kanban — Semana 2
**Herramienta:** Claude 
**Responsable:** Scrum Master 

**¿Para qué se usó?**
Dividir las tareas del TP1 por integrante según rol 
y semana objetivo.

**¿Qué generó la IA?**
Tabla de 8 tareas asignadas a cada rol con semana objetivo.

**¿Qué modificamos y por qué?**
- Ajustamos las semanas según el calendario real del 
  cuatrimestre.
- Reasignamos la tarea de AI_LOG al QA Lead por ser 
  quien tiene mayor control del proceso de calidad.

## Entrada 007

## Herramienta utilizada
Claude (Anthropic) – claude.ai

## Partes generadas con IA
- Prototipo navegable HTML/CSS/JS de las 5 pantallas del sistema
- Capturas PNG de cada pantalla


## Qué modificamos / revisamos
- Verificamos que las clases propuestas (StockSubject, AlertaObserver,
  ReporteStrategy, etc.) reflejen correctamente los patrones GoF
- Adaptamos los nombres de clases a las convenciones del proyecto
- Ajustamos los datos de ejemplo para que sean consistentes con
  el dominio real (ferretería)

## Justificación del uso
Se utilizó IA para acelerar el diseño visual del prototipo (que no
es el núcleo evaluado del TP) y para obtener una segunda opinión
sobre la justificación técnica de los patrones. Las decisiones de
diseño (qué patrón usar, por qué, qué clases involucrar) fueron
tomadas y comprendidas por el equipo antes de la generación.

## Uso crítico
La IA propuso inicialmente usar Singleton para el servicio de alertas.
Se descartó porque Singleton resuelve instancia única, no el problema
de notificación desacoplada. Se mantuvo Observer por ser el patrón
correcto para el problema.

## Entrada 008 — Implementación del patrón Strategy para exportación de reportes
**Herramienta:** Gemini 3.1 Pro

**Responsable:** QA Lead

**¿Para qué se usó?** 
Desarrollar el código en Java del patrón de diseño Strategy para cumplir con el requerimiento de exportar el inventario de la ferretería en múltiples formatos (PDF y Excel/CSV), e integrarlo al código base del sistema.

**¿Qué generó la IA?** 
El código fuente de la interfaz ReporteStrategy, las estrategias concretas ReporteExcel y ReportePDF, la clase de contexto GeneradorReportes, y la actualización completa de la clase Main.java incluyendo la nueva opción del menú y la ejecución dinámica de la estrategia.

**¿Qué modificamos y por qué?**
Agrupamos las nuevas clases dentro de un paquete específico llamado strategy para mantener la coherencia y el orden con la estructura de carpetas que ya venía usando el equipo (ej: paquete observer).

Verificamos que el código de la IA consumiera correctamente los atributos y métodos reales del modelo existente (como getStockActual() y getCategoria().getNombre() de la clase Producto) para asegurar una integración sin errores.

Validamos y aceptamos la decisión de simular la generación de los archivos mediante consola, ya que demuestra la correcta aplicación arquitectónica del patrón sin necesidad de sobrecargar el TP con librerías externas complejas.

