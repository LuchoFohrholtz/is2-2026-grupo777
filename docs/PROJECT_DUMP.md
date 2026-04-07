# FerreStock — Project Dump

> Documento de contexto del proyecto para el repositorio.  
> IS2 · UCP · 2026

---

## Descripción general

FerreStock es un sistema web de gestión de inventario para una ferretería mediana. Permite registrar productos, controlar entradas y salidas de stock, alertar ante stock bajo y generar órdenes de reposición automáticas.

**Stack tecnológico:**
- Backend: Python 3.11 + Flask + Flask-CORS
- Frontend: HTML5 + CSS3 + JavaScript vanilla (fetch API)
- Almacenamiento: en memoria (primera etapa — TP1)
- Patrones de diseño: Observer, Strategy

---

## Estructura del proyecto

```
ferrestock/
├── app.py                  # API REST (Flask) — rutas y controladores
├── index.html              # Frontend SPA — interfaz del usuario
├── requirements.txt        # Dependencias Python
├── src/
│   ├── __init__.py
│   └── models.py           # Modelos del dominio + patrones de diseño
├── docs/
│   ├── patrones-tp1.md     # Documentación de patrones (entregable TP1)
│   └── AI_LOG.md           # Registro de uso de IA (entregable TP1)
├── tests/                  # (vacío — se trabaja en TP2)
└── design/                 # (vacío — diagramas pendientes)
```

---

## Modelos del dominio

### Producto
Entidad central del sistema. Es el **sujeto** del patrón Observer. Notifica a sus observadores cuando `stock_actual < stock_minimo`.

Atributos: `id`, `nombre`, `descripcion`, `precio`, `stock_actual`, `stock_minimo`, `categoria`

Métodos clave:
- `registrar_salida(cantidad, motivo)` → descuenta stock, notifica si hay bajo stock
- `registrar_entrada(cantidad, motivo)` → incrementa stock
- `agregar_observador(obs)` → registra un observador
- `_notificar()` → dispara todos los observadores

### StockMovimiento
Registra cada entrada o salida de stock. Permite trazabilidad completa.

Atributos: `id`, `producto_id`, `producto_nombre`, `cantidad`, `tipo` (entrada/salida), `motivo`, `fecha`

### Categoria
Agrupa productos por rubro. Relación de agregación con Producto.

### Empleado
Actor del sistema. Registra movimientos de stock. (Definido en models.py, integración pendiente con login)

---

## Patrones de diseño implementados

### 1. Observer

**Clases involucradas:**
- `Observador` (ABC): interfaz base
- `Producto`: sujeto — mantiene lista de observadores, notifica al cambiar stock
- `Alerta`: observador concreto — guarda historial de alertas de stock bajo
- `OrdenReposicion`: observador concreto — genera órdenes automáticas de reposición

**Flujo:**
```
Producto.registrar_salida()
    → stock_actual < stock_minimo?
        → Producto._notificar()
            → Alerta.actualizar(producto)
            → OrdenReposicion.actualizar(producto)
```

**Problema que resuelve:** desacoplar la lógica de negocio (manejo de stock) de las reacciones secundarias (alertas, órdenes). Permite agregar nuevos observadores sin modificar `Producto`.

### 2. Strategy

**Clases involucradas:**
- `EstrategiaReporte` (ABC): interfaz base
- `GeneradorReporte`: contexto — delega en la estrategia configurada
- `ReporteReposicion`: estrategia concreta — filtra productos con stock bajo mínimo
- `ReporteStockActual`: estrategia concreta — devuelve todos los productos con estado

**Flujo:**
```
GET /api/reportes/reposicion
    → GeneradorReporte(ReporteReposicion()).ejecutar(productos)

GET /api/reportes/stock
    → GeneradorReporte(ReporteStockActual()).ejecutar(productos)
```

**Problema que resuelve:** agregar nuevos tipos de reporte sin modificar el generador. La estrategia puede cambiarse en tiempo de ejecución con `cambiar_estrategia()`.

---

## API REST — Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Sirve el frontend (index.html) |
| GET | `/api/productos` | Lista todos los productos |
| POST | `/api/productos` | Crea un producto nuevo |
| GET | `/api/movimientos` | Lista todos los movimientos |
| POST | `/api/movimientos` | Registra una entrada o salida |
| GET | `/api/alertas` | Lista el historial de alertas |
| GET | `/api/reportes/reposicion` | Reporte de productos a reponer |
| GET | `/api/reportes/stock` | Reporte completo de stock actual |
| GET | `/api/stats` | Estadísticas generales del sistema |

### Ejemplo: Registrar salida (POST /api/movimientos)

**Request:**
```json
{
  "producto_id": 1,
  "cantidad": 3,
  "tipo": "salida",
  "motivo": "Venta al cliente"
}
```

**Response 201:**
```json
{
  "movimiento": { "id": 1, "producto": "Martillo 500g", "cantidad": 3, "tipo": "salida", "fecha": "07/04/2026 10:30" },
  "producto": { "id": 1, "stock_actual": 5, "bajo_stock": false, ... },
  "notificaciones": []
}
```

---

## Caso de uso principal: Registrar Salida de Stock

**Actor:** Empleado  
**Precondición:** El producto existe en el sistema con stock mayor a cero.  
**Postcondición:** El stock queda actualizado; si cae bajo el mínimo, se generan alerta y orden de reposición.

**Flujo principal:**
1. El empleado selecciona un producto
2. El sistema verifica la disponibilidad de stock
3. El empleado ingresa la cantidad y motivo
4. El sistema registra el movimiento y actualiza el stock
5. Si `stock_actual < stock_minimo`, el sistema genera una alerta y una orden de reposición automática

**Casos de uso incluidos** (`«include»`):
- Buscar producto
- Verificar stock disponible
- Actualizar stock

**Casos de uso extendidos** (`«extend»`, condicionales):
- Generar alerta de stock bajo
- Generar orden de reposición

---

## Estado del proyecto

### TP1 (actual)
- [x] Modelo básico del dominio
- [x] API REST funcional (Flask)
- [x] Frontend básico (HTML/CSS/JS)
- [x] Patrón Observer implementado
- [x] Patrón Strategy implementado
- [x] Datos de prueba (seed)
- [x] Documentación de patrones (`docs/patrones-tp1.md`)
- [x] AI LOG (`docs/AI_LOG.md`)

### Pendiente (TP2+)
- [ ] Base de datos persistente (SQLite o similar)
- [ ] Sistema de login / autenticación
- [ ] Diagrama de caso de uso (en `design/`)
- [ ] Tests unitarios
- [ ] Mejoras de interfaz

---

## Cómo ejecutar

```bash
# Instalar dependencias
pip install flask flask-cors

# Iniciar el servidor
python app.py

# Acceder al sistema
http://localhost:5000
```

---

## Datos de prueba (seed)

Al iniciar, el sistema carga 8 productos de ejemplo:

| Nombre | Categoría | Precio | Stock | Mínimo |
|--------|-----------|--------|-------|--------|
| Martillo 500g | Herramientas | $1500 | 8 | 5 |
| Destornillador Ph | Herramientas | $800 | 3 | 5 |
| Cable 2.5mm x mt | Electricidad | $350 | 20 | 10 |
| Llave de paso 1/2 | Plomería | $2200 | 2 | 4 |
| Látex blanco 4L | Pinturas | $3800 | 12 | 6 |
| Tornillos 4x40 | Fijaciones | $650 | 50 | 20 |
| Cinta aisladora | Electricidad | $300 | 7 | 5 |
| Lija grano 120 | Herramientas | $180 | 4 | 8 |

> Nota: Destornillador Ph (stock 3 < mínimo 5), Llave de paso 1/2 (stock 2 < mínimo 4) y Lija grano 120 (stock 4 < mínimo 8) arrancan en estado de bajo stock.

---

*Generado el 07/04/2026 — FerreStock IS2 · UCP · 2026*
