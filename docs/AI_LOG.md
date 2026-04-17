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

## Entrada 009 — Dividisión de las tareas del TP1
**Herramienta:** Claude (Anthropic)
**Responsable:** Scrum Master 

**¿Para qué se usó?**
Dividir las tareas del TP1 en tarjetas para el tablero Kanban,
asignadas por rol e integrante con eje y semana objetivo.

**¿Qué generó la IA?**
Tabla de 8 tareas con nombre, eje (1, 2 o 3), semana objetivo
y responsable asignado según el rol de cada integrante.

**¿Qué modificamos y por qué?**
- Ajustamos las semanas objetivo al calendario real
  del cuatrimestre.
- Corregimos el eje de la tarea del AI_LOG de Eje 2 a Eje 1
  porque corresponde a proceso y gestión, no a patrones.
- Reordenamos las tareas por dependencia antes de
  cargarlas al tablero.

 ## Entrada 010 — Redactacción del archivo docs/patrones-tp1.md
**Herramienta:** Claude (Anthropic)
**Responsable:** Scrum Master 

**¿Para qué se usó?**
Redactar el archivo docs/patrones-tp1.md con la documentación
completa de los dos patrones implementados para subir al repositorio.

**¿Qué generó la IA?**
Documento Markdown con estructura para Observer y Strategy:
nombre, intención GoF, problema identificado en el sistema,
justificación de la elección, estructura del patrón, implementación
en código Python y mejoras que aporta al sistema.

**¿Qué modificamos y por qué?**
- Reemplazamos las citas textuales de GoF por paráfrasis propias
  para que el documento refleje la comprensión del equipo.
- Ajustamos los ejemplos de código para que coincidan exactamente
  con las clases implementadas en src/models.py.
- Agregamos la sección de alternativas descartadas porque
  la rúbrica del coloquio evalúa específicamente ese punto
  (Dimensión 3 — justificación de decisiones de diseño). 

---

## Entrada 011 — Actualización del Login y Migración a Supabase — Semana de TP2

**Herramienta:** Antigravity AI (Google DeepMind) — asistente de codificación  
**Responsable:** Dev Lead  
**Commit de referencia:** `86ecb8c` — _"Se actualizo el login"_ (Thu Apr 16 2026)

**¿Para qué se usó?**  
Rediseñar la pantalla de login con una estética neon/graffiti urbana, migrar el backend de modelos en memoria a Supabase (base de datos relacional en la nube), y agregar funcionalidades nuevas al sistema (campana de alertas, doble precio costo/venta, carrito de ventas y margen de ganancia configurable).

**¿Qué generó la IA?**

| Archivo | Tipo de cambio | Descripción |
|---|---|---|
| `src/index.html` | Modificado | Rediseño completo del login con fondo oscuro tipo pared urbana, tags de graffiti SVG decorativos, card con borde neon pulsante (`neonPulse`), logo flotante con glow azul, inputs dark-mode y botón redondeado con gradiente. Además: nueva campana de notificaciones con dropdown, badge de alertas en tabs de navegación, ajuste del header (flex + bell-wrap), y estilos CSS compactados. |
| `src/app.py` | Modificado (506 líneas → completo) | Migración de todos los endpoints de modelos Python en memoria a consultas Supabase. Rutas nuevas: `/api/login`, `/api/productos` (GET/POST), `/api/productos/<id>` (PUT/DELETE), `/api/movimientos`, `/api/alertas`, `/api/ordenes`, `/api/ventas` (carrito + venta_items), `/api/stats`, `/api/config/margen`, `/api/exportar/<tipo>`. `exportar_excel` actualizado para mostrar `precio_costo` y `precio_venta` en columnas separadas (9 columnas en vez de 7). |
| `src/models.py` | Modificado | Eliminadas las clases de dominio en memoria (`Producto`, `Categoria`, `StockMovimiento`, `Empleado`) porque la persistencia se delega a Supabase. Se mantuvieron y adaptaron los patrones GoF: Observer (`Observador`, `AlertaObserver`, `OrdenReposicionObserver`), Strategy (`EstrategiaReporte`, `ReporteReposicion`, `ReporteStockActual`, `GeneradorReporte`). Los métodos `generar()` ahora operan sobre diccionarios `p["campo"]` en vez de objetos Python. Agregado comentario explicativo al patrón Strategy. |
| `src/database.py` | **NUEVO** | Módulo de conexión a Supabase usando `postgrest` + `httpx` directamente (sin la librería oficial `supabase-py` para evitar dependencias conflictivas). Clase `SupabaseDB` con timeout de 10 s, lee `SUPABASE_URL`, `SUPABASE_KEY` y `MARGEN_GANANCIA` desde `.env`. Exporta instancia global `supabase`. |
| `setup_db.sql` | **NUEVO** | Script SQL completo para Supabase Dashboard con 6 tablas: `productos` (precio_costo, precio_venta, stock, categoría), `movimientos`, `alertas`, `ordenes_reposicion`, `ventas`, `venta_items`. Incluye políticas RLS permisivas para clave `anon`. |
| `.gitignore` | **NUEVO** | Ignora `.env`, `__pycache__`, `.vscode`, `.idea`, `.DS_Store`, `Thumbs.db` y artefactos de build de Python. |
| `src/requirements.txt` | Modificado | Agregadas dependencias `supabase` y `python-dotenv`. |
| `src/logo.png` | **NUEVO** | Logo de FerreRAP añadido al directorio `src/` para ser referenciado en la pantalla de login. |

**¿Qué modificamos y por qué?**
- Rechazamos la dependencia oficial `supabase-py` porque instala `pyiceberg` y `storage3`, que generaban conflictos de versiones en Windows. Se reemplazó por `postgrest` + `httpx` puro.
- El panel de login generado inicialmente no incluía el logo flotante sobre la card; se ajustó el `z-index` y el `margin-bottom` negativo para lograr el efecto superpuesto.
- Los reportes Excel pasaron de 7 a 9 columnas para mostrar `precio_costo` y `precio_venta` por separado, alineándose con el modelo de negocio real de la ferretería (precio de compra ≠ precio de venta).
- La animación `neonPulse` se calibró manualmente para que el pulso no fuera agresivo (3 s, amplitud moderada).
- Se validó que las políticas RLS del SQL permitan acceso anónimo durante el desarrollo; se recomienda restringir en producción.

**Uso crítico de la IA:**  
La IA propuso inicialmente usar la librería oficial `supabase-py` para la integración. El equipo detectó que esto arrastraba dependencias innecesarias (`pyiceberg`, `storage3`) que rompían el entorno en Windows. Se discutió la alternativa y se decidió implementar `SupabaseDB` directamente sobre `postgrest` + `httpx`, lo que demostró comprensión del protocolo REST de Supabase en lugar de depender de una abstracción opaca.

