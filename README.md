# is2-2026- nipintucu
## Descripción del Proyecto
Desarrollamos un sistema web de gestión de inventario para una ferretería que permite registrar productos y controlar el stock en tiempo real.

## Equipo de Trabajo

| Nombre              | Rol          | GitHub           | 
|---------------------|--------------|------------------| 
| Santiago Gonzalez   | Scrum Master | [@santi-ngonzalez](https://github.com/santi-ngonzalez) | 
| Luciano Fohrholtz   | Dev Lead     | [@luchofohrholz](https://github.com/luchofohrholtz)|
| Juan Carlos Abente  | QA Lead      | [@juankiabente](https://github.com/juankiabente)|
| Mariano Acosta      | UX Lead      | [@mittax6](https://github.com/mittax6) |

## Enlaces Rápidos
* [Tablero Kanban (GitHub Projects)](https://github.com/users/LuchoFohrholtz/projects/1)
* [Matriz de Riegos](https://github.com/LuchoFohrholtz/is2-2026-nipintucu/blob/main/docs/matriz-de-riesgos.md)
* [AI Log](https://github.com/LuchoFohrholtz/is2-2026-nipintucu/blob/main/docs/contrato-de-proyecto.md).
* [Informe TP1](https://docs.google.com/document/d/1C3rg_HAe2fNjk1P0o_SO_F86wyOYUDYX/edit?usp=sharing&ouid=105019262908114217359&rtpof=true&sd=true)
* [Documentación de Patrones de Diseño](https://github.com/LuchoFohrholtz/is2-2026-nipintucu/blob/main/docs/patrones-tp1.md). 

## Diagrama de clases
<img width="6272" height="3235" alt="Untitled diagram-2026-03-28-111951 (1)" src="https://github.com/user-attachments/assets/4464cde6-9036-492d-a27b-fdf38a3fd215" />
<img width="5389" height="3235" alt="Electric Tools Stock-2026-03-28-111225 (1)" src="https://github.com/user-attachments/assets/ab07e319-33f1-48cd-bc08-a98e513f6fe5" />

## Tecnologías utilizadas
| Tecnología          | Uso          | 
|---------------------|--------------|
| Python 3.12   | Lenguaje principal del backend |  
| Flask   | API REST     | 
| HTML / CSS / JS  | Interfaz web     | 
| GitHub Projects      | Tablero Kanban     |
| Figma | Prototipo de interfaz |

## Patrones de diseño implementados
### Observer — Comportamental
Aplicado entre Producto y los observadores Alerta y OrdenReposicion.
Cuando el stock de un producto cae por debajo del mínimo configurado, el sistema notifica automáticamente a todos los observadores registrados sin que Producto conozca sus implementaciones.
### Strategy — Comportamental
Aplicado en el módulo de reportes a través de GeneradorReporte y las estrategias ReporteReposicion y ReporteStockActual.
Permite intercambiar el algoritmo de generación de reportes en tiempo de ejecución sin modificar el código del contexto.

## Caso de uso principal
### Registrar una salida de stock y generar alerta si el stock queda bajo mínimo
* 1- El empleado registra una salida de stock con producto, cantidad y motivo.
* 2- El sistema descuenta el stock actual del producto.
* 3- Si stock_actual < stock_minimo, el patrón Observer notifica automáticamente a Alerta y OrdenReposicion.
* 4- La alerta queda registrada y visible en el panel de alertas.

## Uso de IA
El equipo utilizó herramientas de IA durante el desarrollo.
Todo el uso está documentado con detalle en: [AI Log](https://github.com/LuchoFohrholtz/is2-2026-nipintucu/blob/main/docs/contrato-de-proyecto.md).
