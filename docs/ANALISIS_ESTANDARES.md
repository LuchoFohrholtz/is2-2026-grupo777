# Análisis de Estándares — FerreRAP
**Materia:** Ingeniería de Software II · UCP · 2026  
**Sistema:** FerreRAP — Gestión de Stock para Ferretería  
**Equipo:** Santiago Gonzalez · Luciano Fohrholtz · Juan Carlos Abente · Mariano Acosta

---

## 1. Tabla comparativa de estándares

| Estándar | Año | Enfoque principal | ¿Aplica a nuestro proyecto? | Justificación |
|---|---|---|---|---|
| **ISO 9241-11** | 1998 (rev. 2018) | Usabilidad: eficacia, eficiencia y satisfacción del usuario en la interacción con el sistema. | ✅ Sí — directamente | FerreRAP es operado por empleados de mostrador y encargados de compras. La eficacia con la que registran ventas, interpretan alertas y reponen stock impacta directamente en la operativa diaria de la ferretería. |
| **ISO 13407** | 1999 (reemplazada por ISO 9241-210) | Proceso de diseño centrado en el humano: 4 pasos iterativos (contexto de uso, requisitos, soluciones de diseño, evaluación). | ✅ Sí — como proceso | El equipo aplicó iteraciones de diseño entre Sprint 0 y TP1: se identificaron los actores (empleado, encargado), se definieron requisitos funcionales y se evaluó el prototipo con el grupo. El proceso siguió implícitamente los 4 pasos de ISO 13407. |
| **ISO/IEC 27001** | 2005 (rev. 2022) | Seguridad de la información: gestión de riesgos, confidencialidad, integridad y disponibilidad de los datos. | ⚠ Parcialmente | FerreRAP almacena datos de ventas, precios, stock y datos de facturación (nombre, DNI, CUIT del cliente) en Supabase. Aunque no maneja datos de salud ni financieros de alto riesgo, la protección de datos de clientes y la gestión de credenciales de acceso hacen relevante este estándar. |
| **ISA/IEC 62443** | 2007–2018 | Ciberseguridad en sistemas de control industrial: protección de SCADA, PLC y redes de automatización. | ❌ No aplica | FerreRAP es un sistema de gestión web, no un sistema de control industrial. No opera sobre infraestructura física automatizada, sensores ni actuadores. Este estándar aplica a sistemas como líneas de producción, plantas de energía o redes de distribución industrial. |
| **ISO 9001** | 1987 (rev. 2015) | Calidad en procesos: satisfacción del cliente, mejora continua, gestión de no conformidades. | ✅ Sí — como marco de calidad | El uso de Scrum con sprints, criterios de aceptación definidos por el QA Lead, y el tablero Kanban con columnas de revisión son prácticas alineadas con ISO 9001. La trazabilidad de movimientos de stock y el historial de ventas también responden a requisitos de calidad de proceso. |

---

## 2. Análisis aplicado al proyecto

### ¿Cuáles son los estándares más relevantes para nuestro escenario?

Los más relevantes son **ISO 9241-11** e **ISO 9001**. FerreRAP opera en un entorno comercial donde la usabilidad es crítica: los empleados de mostrador deben poder registrar ventas rápidamente sin cometer errores. ISO 9241-11 define exactamente eso — eficacia, eficiencia y satisfacción. Por otro lado, ISO 9001 es relevante porque el sistema gestiona procesos de negocio reales (compras, ventas, alertas de stock) que requieren trazabilidad, control de calidad y mejora continua.

### ¿Qué estándares debería cumplir si el sistema fuera declarado crítico?

Si FerreRAP formara parte de un entorno crítico — por ejemplo, si la ferretería proveyera insumos a una planta industrial o si el sistema manejara fondos significativos — debería cumplir obligatoriamente:

- **ISO/IEC 27001**: para proteger los datos de clientes, credenciales de acceso y registros de transacciones ante ataques o filtraciones.
- **ISO 9001**: para garantizar que los procesos de stock, reposición y venta estén documentados, auditados y mejoren continuamente.
- **ISA/IEC 62443**: solo si el sistema se integrara con maquinaria automatizada del depósito o sensores de inventario físico.

### ¿Qué concepto de ISO 13407 o ISO 9241-11 sigue siendo útil hoy en sistemas críticos?

El concepto más vigente de **ISO 13407** es la **iteración centrada en el usuario**: diseñar, evaluar con usuarios reales, y rediseñar. En sistemas críticos esto es esencial — un operador que comete un error en una interfaz confusa puede generar consecuencias graves. El concepto más útil de **ISO 9241-11** es la **eficacia**: que el usuario pueda completar su tarea sin errores. En sistemas críticos, un solo error de operación puede ser irreversible.

---

## 3. Conclusión

Si tuviéramos que certificar FerreRAP bajo un estándar actual, elegiríamos **ISO 9001** como punto de partida por su alcance en gestión de procesos y mejora continua, combinado con **ISO 9241-11** para asegurar que la interfaz sea usable por personal no técnico. La certificación ISO 9001 implicaría formalizar los criterios de aceptación de cada funcionalidad, documentar los procesos de registro de ventas y reposición, y establecer métricas de calidad medibles. En cuanto al diseño, requeriría revisar el flujo de ventas para agregar confirmaciones explícitas y la posibilidad de anular operaciones, alineado también con la Heurística 3 de Nielsen. Respecto a la arquitectura, el patrón **Observer** facilita el cumplimiento de ISO 9001 porque garantiza que cada cambio de estado crítico (stock bajo) dispara acciones automáticas y trazables. El patrón **Strategy** también colabora, ya que permite cambiar los algoritmos de reporte sin modificar el sistema central, lo que reduce el riesgo de introducir errores en procesos auditados.

---

## 4. Relación entre decisiones de diseño del TP1 y los estándares

| Decisión de diseño | Estándar relacionado | ¿Ayuda o dificulta? |
|---|---|---|
| Patrón Observer (notificación automática de stock bajo) | ISO 9001 — trazabilidad de procesos | ✅ Ayuda: cada evento crítico queda registrado automáticamente en Supabase sin depender de la acción manual del usuario. |
| Patrón Strategy (reportes intercambiables) | ISO 9001 — mejora continua | ✅ Ayuda: agregar nuevos tipos de reporte no modifica el código existente, lo que reduce riesgos en procesos auditados. |
| Login con roles (Administrador / Empleado) | ISO/IEC 27001 — control de acceso | ✅ Ayuda: la separación de roles es un requisito básico de seguridad de la información. Sin embargo, las credenciales están hardcodeadas en el código, lo que dificulta el cumplimiento completo. |
| Base de datos en Supabase (nube) | ISO/IEC 27001 — disponibilidad y confidencialidad | ⚠ Parcial: Supabase ofrece cifrado en tránsito y en reposo, pero el equipo no configuró políticas de Row Level Security (RLS), lo que es un gap respecto a ISO 27001. |
| Exportación a PDF y Excel | ISO 9001 — documentación de procesos | ✅ Ayuda: los reportes exportables permiten auditar el estado del stock en cualquier momento, cumpliendo el requisito de trazabilidad documental. |

---

*IS II · UCP Inc. · FerreRAP · 2026*
