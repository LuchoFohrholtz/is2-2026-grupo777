#01-inventario.png
KPIs en la parte superior permiten escaneo inmediato sin leer la tabla; las filas con stock bajo se destacan con fondo rojo y borde lateral, aplicando la heurística de visibilidad del estado del sistema (ISO 9241-11, eficacia). La barra de nivel de stock permite comparar porcentualmente de un vistazo.

#02-registrar-movimiento.png
El formulario incluye un panel de vista previa en tiempo real que muestra el stock resultante antes de confirmar, eliminando errores por cálculo mental. El toast de alerta (patrón Observer) aparece inmediatamente al registrar una salida crítica con un link directo a la pantalla de Alertas, reduciendo el número de pasos para el flujo principal (eficiencia).

#03-alertas.png
Las alertas se ordenan por urgencia (críticas primero), con borde lateral coloreado para jerarquía visual inmediata. El badge rojo en la navegación lateral muestra el conteo activo en todo momento (visibilidad persistente del estado). Cada tarjeta expone stock actual vs. mínimo con tipografía de gran tamaño, permitiendo decisión sin entrar al detalle del producto.

#04-reportes.png
Dos cards seleccionables (con borde y checkmark al activarse) hacen explícito que son dos estrategias distintas del mismo generador, reflejando directamente el patrón Strategy. El encabezado del reporte muestra la etiqueta "Strategy A / B" para que sea trazable en el prototipo. Una sola acción genera el reporte sin confirmaciones intermedias (eficiencia).

#05-nuevo-producto.png
El campo de stock mínimo incluye una advertencia contextual amarilla explicando su rol en el sistema de alertas, ayudando al usuario a configurarlo correctamente desde el inicio (prevención de errores, ISO 9241-11). El campo de margen se calcula automáticamente para reducir carga cognitiva.
