# FerreRAP — Project Dump

> Documento de contexto del proyecto para el repositorio.
> IS2 · UCP · 2026 — Grupo nipintucu

---

## Descripción general

FerreRAP es un sistema web de gestión de inventario para una ferretería mediana. Permite registrar productos, controlar entradas y salidas de stock, alertar ante stock bajo y generar órdenes de reposición automáticas.

**Contexto de negocio (Opción B — consigna):**
> Una ferretería mediana necesita controlar su stock. Hoy no saben qué tienen ni cuándo pedir más. Quieren una solución web que les avise cuando un producto está por agotarse.

**Usuarios principales:** Empleado y encargado de compras (Administrador).

**Funcionalidades mínimas cumplidas:**
- [x] Registrar productos con nombre, categoría, precio y stock actual
- [x] Registrar entradas y salidas de stock con fecha y motivo
- [x] Alertar cuando un producto cae por debajo del stock mínimo configurado
- [x] Generar un listado de productos a reponer
- [x] Buscar productos por nombre o categoría

**Stack tecnológico:**

| Tecnología        | Uso                                        |
|-------------------|--------------------------------------------|
| Python 3.12       | Lenguaje principal del backend             |
| Flask 3.0.0       | API REST                                   |
| flask-cors 4.0.0  | CORS                                       |
| reportlab 4.2.0   | Exportación PDF                            |
| openpyxl 3.1.2    | Exportación Excel (.xlsx)                  |
| HTML5 / CSS3 / JS | SPA frontend (fetch API, todo en 1 archivo)|
| GitHub Projects   | Tablero Kanban                             |

---

## Equipo

| Nombre             | Rol          | GitHub                                                   |
|--------------------|--------------|----------------------------------------------------------|
| Santiago Gonzalez  | Scrum Master | [@santi-ngonzalez](https://github.com/santi-ngonzalez)  |
| Luciano Fohrholtz  | Dev Lead     | [@luchofohrholz](https://github.com/luchofohrholz)      |
| Juan Carlos Abente | QA Lead      | [@juankiabente](https://github.com/juankiabente)         |
| Mariano Acosta     | UX Lead      | [@mittax6](https://github.com/mittax6)                   |

---

## Consigna y objetivo del TP1

**Objetivo:** Aplicar patrones de diseño (GoF) dentro del sistema del grupo, integrándolos en funcionalidades reales y justificando técnicamente su uso.

### Alcance del TP1

Este trabajo corresponde a la **primera etapa del proyecto**. No se espera un sistema completo, sino una primera versión funcional bien diseñada.

✅ **Lo que se debe alcanzar:**
- Modelo básico del dominio (clases principales + relaciones)
- Funcionalidad mínima operativa — al menos un caso de uso de punta a punta
- Implementación de al menos **2 patrones de diseño reales** dentro del sistema
- Código organizado, separación básica de responsabilidades
- Base preparada para continuar en TP2

❌ **Lo que NO se espera en este TP:**
- Sistema completo
- Persistencia compleja (base de datos)
- Testing completo (se trabaja en TP2)
- Optimización final

### Documentación obligatoria entregada

- `docs/patrones-tp1.md` — Documentación de patrones (nombre, intención, problema, justificación, código)
- `docs/AI_LOG.md` — Registro de uso de IA (herramienta, partes generadas, modificaciones, justificación)

---

## Estructura del proyecto

```
is2-2026-nipintucu/
├── README.md
├── docs/
│   ├── AI_LOG.md                          # Registro de uso de IA (entregable TP1)
│   ├── PROJECT_DUMP.md                    # Este documento
│   ├── contrato-de-proyecto.md
│   ├── matriz-de-riesgos.md
│   ├── patrones-tp1.md                    # Documentación de patrones (entregable TP1)
│   ├── Primer modelo de Protoclases.jpeg
│   ├── protoclase 1 - movimiento cliente.jpg
│   └── protoclase 2 - moviemiento proveedor.png
├── src/
│   ├── __init__.py
│   ├── .gitkeep
│   ├── app.py          # API REST Flask — rutas y controladores (468 líneas)
│   ├── index.html      # Frontend SPA — interfaz del usuario (1303 líneas)
│   ├── models.py       # Modelos del dominio + patrones Observer y Strategy (306 líneas)
│   └── requirements.txt
└── tests/
    └── .gitkeep        # (vacío — se trabaja en TP2)
```

---

## Modelos del dominio (`src/models.py`)

### `Producto`
Entidad central del sistema. Es el **sujeto** del patrón Observer. Notifica a sus observadores cuando `stock_actual < stock_minimo`.

**Atributos:** `id`, `nombre`, `descripcion`, `precio`, `stock_actual`, `stock_minimo`, `categoria`, `_observadores`, `ultimas_notificaciones`

**Métodos clave:**
- `registrar_salida(cantidad, motivo)` → descuenta stock; si queda bajo mínimo, dispara `_notificar()`
- `registrar_entrada(cantidad, motivo)` → incrementa stock; si supera mínimo, dispara `_notificar_reposicion()`
- `agregar_observador(obs)` → registra un observador en la lista interna
- `_notificar()` → llama a `actualizar(self)` en cada observador
- `_notificar_reposicion()` → llama a `resolver(self)` en cada observador
- `bajo_stock` (property) → `stock_actual < stock_minimo`
- `to_dict()` → serialización JSON

### `StockMovimiento`
Registra cada entrada o salida de stock. Permite trazabilidad completa del inventario.

**Atributos:** `id`, `producto_id`, `producto_nombre`, `cantidad`, `tipo` (`entrada`/`salida`), `motivo`, `fecha`

### `Categoria`
Agrupa productos por rubro. Relación de **agregación** con `Producto` (existe aunque no tenga productos asignados).

### `Empleado`
Actor del sistema. Registra movimientos de stock. Definido en `models.py`; autenticación gestionada en `app.py` con `USUARIOS` dict por ahora.

---

## Patrones de diseño implementados

> **Consigna:** Para cada patrón se debe poder explicar: qué problema existía, por qué se eligió y qué mejora aporta.

---

### Patrón 1 — Observer (Comportamental)

#### Intención (GoF)
Define una dependencia de uno a muchos entre objetos, de forma que cuando un objeto cambia de estado, todos sus dependientes son notificados y actualizados automáticamente.

#### Problema que existía en el sistema
Al registrar una salida de stock, el sistema necesitaba reaccionar de múltiples formas: generar una alerta visible y crear una orden de reposición. Sin Observer, `Producto` tendría que conocer y llamar directamente a `Alerta` y `OrdenReposicion`, creando acoplamiento fuerte. Agregar una nueva reacción (ej: enviar email) implicaría modificar `Producto`.

#### Por qué se eligió Observer
Permite que `Producto` solo conozca la interfaz `Observador` y notifique a quien esté suscripto, sin saber quién ni cuántos son. El desacoplamiento es total: agregar un nuevo observador no requiere tocar `Producto`.

#### Qué mejora aporta
- **Desacoplamiento:** `Producto` no conoce las implementaciones concretas de `Alerta` ni `OrdenReposicion`
- **Extensibilidad:** se puede agregar `EmailObserver`, `LogObserver`, etc. sin modificar código existente
- **Mantenibilidad:** cada observador tiene una responsabilidad única y clara

#### Clases involucradas

| Clase            | Rol               | Descripción                                                  |
|------------------|-------------------|--------------------------------------------------------------|
| `Observador`     | Interfaz (ABC)    | Define `actualizar(producto)` y `resolver(producto)`         |
| `Producto`       | Sujeto            | Mantiene lista `_observadores`, notifica al modificar stock  |
| `Alerta`         | Observador concreto | Guarda historial de alertas de stock bajo                  |
| `OrdenReposicion`| Observador concreto | Genera y gestiona órdenes automáticas de reposición        |

#### Flujo de notificación

```
Producto.registrar_salida(cantidad, motivo)
    → self.stock_actual -= cantidad
    → if self.bajo_stock:
        → self._notificar()
            → Alerta.actualizar(producto)      # → agrega entrada a historial
            → OrdenReposicion.actualizar(producto) # → crea orden "pendiente"

Producto.registrar_entrada(cantidad, motivo)
    → self.stock_actual += cantidad
    → if not self.bajo_stock:
        → self._notificar_reposicion()
            → Alerta.resolver(producto)            # → registra normalización
            → OrdenReposicion.resolver(producto)   # → cierra órdenes pendientes
```

#### Ejemplo en el código (`src/models.py`)

```python
class Observador(ABC):
    @abstractmethod
    def actualizar(self, producto): pass
    def resolver(self, producto): return None

class Alerta(Observador):
    def __init__(self):
        self.historial = []
    def actualizar(self, producto):
        entrada = {
            "tipo": "alerta",
            "mensaje": f"Stock bajo en '{producto.nombre}'",
            "stock_actual": producto.stock_actual,
            "stock_minimo": producto.stock_minimo,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        self.historial.append(entrada)
        return entrada

class Producto:  # Sujeto
    def _notificar(self):
        self.ultimas_notificaciones = []
        for obs in self._observadores:
            resultado = obs.actualizar(self)
            if resultado:
                self.ultimas_notificaciones.append(resultado)
```

---

### Patrón 2 — Strategy (Comportamental)

#### Intención (GoF)
Define una familia de algoritmos, encapsula cada uno y los hace intercambiables. Permite que el algoritmo varíe independientemente de los clientes que lo usan.

#### Problema que existía en el sistema
El sistema necesitaba generar distintos tipos de reporte: uno con solo los productos a reponer y otro con el stock completo. Sin Strategy, `GeneradorReporte` tendría condicionales (`if tipo == "reposicion"`) que crecen con cada nuevo reporte. Agregar un nuevo tipo requeriría modificar la clase central.

#### Por qué se eligió Strategy
Encapsula cada algoritmo de reporte en su propia clase. `GeneradorReporte` solo conoce la interfaz `EstrategiaReporte` y delega en ella. El tipo de reporte puede cambiarse en tiempo de ejecución con `cambiar_estrategia()`.

#### Qué mejora aporta
- **Flexibilidad:** agregar `ReporteCategoria`, `ReportePorFecha`, etc. sin tocar `GeneradorReporte`
- **Principio Open/Closed:** abierto a extensión, cerrado a modificación
- **Legibilidad:** cada estrategia tiene una responsabilidad clara y aislada

#### Clases involucradas

| Clase                 | Rol                  | Descripción                                              |
|-----------------------|----------------------|----------------------------------------------------------|
| `EstrategiaReporte`   | Interfaz (ABC)       | Define `generar(productos)`                              |
| `GeneradorReporte`    | Contexto             | Delega en la estrategia configurada; expone `ejecutar()` |
| `ReporteReposicion`   | Estrategia concreta  | Filtra solo productos con `stock_actual < stock_minimo`  |
| `ReporteStockActual`  | Estrategia concreta  | Devuelve todos los productos con campo `bajo_stock`      |

#### Flujo de ejecución

```
GET /api/reportes/reposicion
    → GeneradorReporte(ReporteReposicion()).ejecutar(productos)
        → ReporteReposicion.generar(productos)  # filtra bajo stock

GET /api/reportes/stock
    → GeneradorReporte(ReporteStockActual()).ejecutar(productos)
        → ReporteStockActual.generar(productos) # todos los productos

# Misma lógica para PDF y Excel:
GET /api/reportes/stock/pdf
    → GeneradorReporte(ReporteStockActual()).ejecutar(productos) → reportlab → .pdf
```

#### Ejemplo en el código (`src/models.py`)

```python
class EstrategiaReporte(ABC):
    @abstractmethod
    def generar(self, productos): pass

class ReporteReposicion(EstrategiaReporte):
    def generar(self, productos):
        return [p.__dict__ for p in productos if p.stock_actual < p.stock_minimo]

class ReporteStockActual(EstrategiaReporte):
    def generar(self, productos):
        return [{**p.__dict__, "bajo_stock": p.stock_actual < p.stock_minimo}
                for p in productos]

class GeneradorReporte:          # Contexto
    def __init__(self, estrategia: EstrategiaReporte):
        self._estrategia = estrategia
    def cambiar_estrategia(self, estrategia: EstrategiaReporte):
        self._estrategia = estrategia
    def ejecutar(self, productos):
        return self._estrategia.generar(productos)
```

---

## API REST — Endpoints completos

| Método | Ruta                            | Descripción                                      |
|--------|---------------------------------|--------------------------------------------------|
| POST   | `/api/login`                    | Autenticación (usuario + contraseña)             |
| GET    | `/`                             | Sirve el frontend (`index.html`)                 |
| GET    | `/api/productos`                | Lista todos los productos                        |
| POST   | `/api/productos`                | Crea un producto nuevo (valida todos los campos) |
| GET    | `/api/movimientos`              | Lista todos los movimientos (orden inverso)      |
| POST   | `/api/movimientos`              | Registra una entrada o salida de stock           |
| GET    | `/api/alertas`                  | Lista el historial de alertas (Observer)         |
| GET    | `/api/reportes/reposicion`      | Reporte JSON — productos a reponer               |
| GET    | `/api/reportes/stock`           | Reporte JSON — stock completo con estado         |
| GET    | `/api/reportes/reposicion/pdf`  | Descarga PDF — productos a reponer (reportlab)   |
| GET    | `/api/reportes/stock/pdf`       | Descarga PDF — stock completo                    |
| GET    | `/api/reportes/reposicion/excel`| Descarga .xlsx — productos a reponer (openpyxl)  |
| GET    | `/api/reportes/stock/excel`     | Descarga .xlsx — stock completo                  |
| GET    | `/api/stats`                    | Estadísticas globales del sistema                |

### Ejemplo: Registrar salida (POST `/api/movimientos`)

**Request:**
```json
{
  "producto_id": 1,
  "cantidad": 3,
  "tipo": "salida",
  "motivo": "Venta al cliente"
}
```

**Response 201 — sin alerta:**
```json
{
  "movimiento": { "id": 1, "producto": "Martillo 500g", "cantidad": 3, "tipo": "salida", "fecha": "08/04/2026 20:00" },
  "producto": { "id": 1, "stock_actual": 5, "bajo_stock": false },
  "notificaciones": []
}
```

**Response 201 — con Observer disparado:**
```json
{
  "movimiento": { "id": 2, "producto": "Destornillador Ph", "cantidad": 2, "tipo": "salida", "fecha": "08/04/2026 20:01" },
  "producto": { "id": 2, "stock_actual": 1, "bajo_stock": true },
  "notificaciones": [
    { "tipo": "alerta", "mensaje": "Stock bajo en 'Destornillador Ph'", "stock_actual": 1, "stock_minimo": 5 },
    { "tipo": "orden", "mensaje": "Reponer 'Destornillador Ph'", "cantidad_sugerida": 10, "estado": "pendiente" }
  ]
}
```

---

## Caso de uso principal: Registrar salida de stock

**Actor:** Empleado
**Precondición:** El producto existe en el sistema con stock mayor a cero.
**Postcondición:** El stock queda actualizado; si cae bajo el mínimo, se generan alerta y orden de reposición automáticamente.

**Flujo principal:**
1. El empleado selecciona un producto del selector (cargado desde `/api/productos`)
2. El sistema muestra el stock actual disponible
3. El empleado ingresa tipo (`salida`), cantidad y motivo
4. El sistema valida que `cantidad > 0` y `cantidad ≤ stock_actual`
5. El sistema registra el `StockMovimiento` y actualiza el `stock_actual` del producto
6. Si `stock_actual < stock_minimo` → el patrón Observer notifica automáticamente a `Alerta` y `OrdenReposicion`
7. La interfaz muestra el resultado y las notificaciones disparadas

**Casos de uso incluidos** (`«include»`):
- Buscar / seleccionar producto
- Verificar stock disponible
- Actualizar stock

**Casos de uso extendidos** (`«extend»`, condicionales):
- Generar alerta de stock bajo (si `stock_actual < stock_minimo`)
- Generar orden de reposición automática (si `stock_actual < stock_minimo`)

---

## Usuarios del sistema

| Usuario    | Contraseña     | Rol            | Permisos                                              |
|------------|----------------|----------------|-------------------------------------------------------|
| `admin`    | `admin123`     | Administrador  | Todas las secciones incluyendo "Nuevo producto"       |
| `empleado` | `empleado123`  | Empleado       | Inventario, Movimientos, Alertas, Reportes            |

---

## Estado del proyecto

### TP1 (entregado)
- [x] Modelo básico del dominio (`Producto`, `StockMovimiento`, `Categoria`, `Empleado`)
- [x] API REST funcional (Flask) con autenticación básica por rol
- [x] Frontend SPA (HTML/CSS/JS vanilla) con dark mode
- [x] Patrón Observer implementado e integrado (`Alerta`, `OrdenReposicion`)
- [x] Patrón Strategy implementado e integrado (`ReporteReposicion`, `ReporteStockActual`)
- [x] Exportación de reportes a PDF (reportlab) y Excel (openpyxl)
- [x] Búsqueda de productos por nombre y categoría
- [x] Datos de prueba (seed con 8 productos)
- [x] Control de acceso por rol (admin / empleado)
- [x] Documentación de patrones (`docs/patrones-tp1.md`)
- [x] AI LOG (`docs/AI_LOG.md`)

### Pendiente (TP2+)
- [ ] Base de datos persistente (SQLite o similar)
- [ ] Sistema de login con sesiones reales / JWT
- [ ] Tests unitarios en `tests/`
- [ ] Diagrama de caso de uso formal

---

## Cómo ejecutar

```bash
# Instalar dependencias
pip install flask flask-cors reportlab openpyxl

# O con requirements.txt
pip install -r src/requirements.txt

# Iniciar el servidor (desde la carpeta src/)
python src/app.py

# Acceder al sistema
http://localhost:5000

# Credenciales
#   admin / admin123      → Administrador (acceso total)
#   empleado / empleado123 → Empleado (sin alta de productos)
```

---

## Datos de prueba (seed)

Al iniciar, el sistema carga 8 productos de ejemplo:

| Nombre             | Categoría    | Precio | Stock | Mínimo | Estado inicial |
|--------------------|--------------|--------|-------|--------|----------------|
| Martillo 500g      | Herramientas | $1500  | 8     | 5      | OK             |
| Destornillador Ph  | Herramientas | $800   | 3     | 5      | ⚠ Bajo stock  |
| Cable 2.5mm x mt   | Electricidad | $350   | 20    | 10     | OK             |
| Llave de paso 1/2  | Plomería     | $2200  | 2     | 4      | ⚠ Bajo stock  |
| Látex blanco 4L    | Pinturas     | $3800  | 12    | 6      | OK             |
| Tornillos 4x40     | Fijaciones   | $650   | 50    | 20     | OK             |
| Cinta aisladora    | Electricidad | $300   | 7     | 5      | OK             |
| Lija grano 120     | Herramientas | $180   | 4     | 8      | ⚠ Bajo stock  |

> **Nota:** Destornillador Ph, Llave de paso 1/2 y Lija grano 120 arrancan en estado de bajo stock — útil para demostrar el Observer desde el inicio.

---

## Uso de IA — Resumen del AI LOG

| Entrada | Herramienta | Responsable       | Uso                                               |
|---------|-------------|-------------------|---------------------------------------------------|
| 001     | ChatGPT     | Dev Lead          | Tabla de integrantes y roles                      |
| 002     | ChatGPT     | Dev Lead          | Estructura del repositorio GitHub                 |
| 003     | ChatGPT     | Scrum / Dev Lead  | Gestión de colaboradores GitHub                   |
| 004     | ChatGPT     | Scrum / Dev Lead  | Estrategias Matriz de Riesgos                     |
| 005     | ChatGPT     | Dev Lead          | Código Mermaid — diagrama de clases               |
| 006     | Claude      | Scrum Master      | División de tareas para el Kanban                 |
| 007     | Claude      | —                 | Prototipo navegable HTML/CSS/JS (5 pantallas)     |
| 008     | Gemini      | QA Lead           | Patrón Strategy para exportación de reportes      |
| 009     | Claude      | Scrum Master      | División TP1 en tarjetas Kanban                   |
| 010     | Claude      | Scrum Master      | Redacción `docs/patrones-tp1.md`                  |

> Detalle completo con qué se generó, qué se modificó y por qué: ver [`docs/AI_LOG.md`](./AI_LOG.md)

---

*Generado el 08/04/2026 — FerreRAP IS2 · UCP · 2026*
