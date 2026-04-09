# Project Dump — FerreRAP · IS2 · UCP · 2026

> Repositorio: `LuchoFohrholtz/is2-2026-nipintucu`  
> Generado: 2026-04-08

---

## Árbol de archivos

```
is2-2026-nipintucu/
├── README.md
├── docs/
│   ├── AI_LOG.md
│   ├── PROJECT_DUMP.md
│   ├── contrato-de-proyecto.md
│   ├── matriz-de-riesgos.md
│   ├── patrones-tp1.md
│   ├── Primer modelo de Protoclases.jpeg
│   ├── protoclase 1 - movimiento cliente.jpg
│   └── protoclase 2 - moviemiento proveedor.png
├── src/
│   ├── __init__.py
│   ├── .gitkeep
│   ├── app.py          (468 líneas — API Flask)
│   ├── index.html      (1303 líneas — SPA frontend)
│   ├── models.py       (306 líneas — dominio + patrones)
│   └── requirements.txt
└── tests/
    └── .gitkeep
```

---

## Equipo

| Nombre             | Rol          | GitHub                                            |
|--------------------|--------------|---------------------------------------------------|
| Santiago Gonzalez  | Scrum Master | [@santi-ngonzalez](https://github.com/santi-ngonzalez) |
| Luciano Fohrholtz  | Dev Lead     | [@luchofohrholz](https://github.com/luchofohrholz)     |
| Juan Carlos Abente | QA Lead      | [@juankiabente](https://github.com/juankiabente)        |
| Mariano Acosta     | UX Lead      | [@mittax6](https://github.com/mittax6)                  |

---

## Stack tecnológico

| Tecnología        | Uso                         |
|-------------------|-----------------------------|
| Python 3.12       | Backend                     |
| Flask 3.0.0       | API REST                    |
| flask-cors 4.0.0  | CORS                        |
| reportlab 4.2.0   | Exportación PDF             |
| openpyxl 3.1.2    | Exportación Excel           |
| HTML / CSS / JS   | SPA frontend (todo en 1 archivo) |

---

## Patrones de diseño implementados

### Observer (Comportamental)
- **Sujeto:** `Producto`
- **Observadores:** `Alerta`, `OrdenReposicion`
- **Trigger:** `stock_actual < stock_minimo`

### Strategy (Comportamental)
- **Contexto:** `GeneradorReporte`
- **Estrategias:** `ReporteReposicion`, `ReporteStockActual`
- **Intercambio en runtime** vía botones del frontend

---

## `src/requirements.txt`

```
flask==3.0.0
flask-cors==4.0.0
reportlab==4.2.0
openpyxl==3.1.2
```

---

## `src/models.py`

```python
"""
FerreStock — Modelos del dominio
Patrones implementados: Observer, Strategy
IS2 · UCP · 2026
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ─────────────────────────────────────────────────────────────
#  PATRÓN OBSERVER
#  Sujeto: Producto
#  Observadores: Alerta, OrdenReposicion
# ─────────────────────────────────────────────────────────────

class Observador(ABC):
    """Interfaz base para todos los observadores del sistema."""

    @abstractmethod
    def actualizar(self, producto):
        """Llamado cuando el stock cae por debajo del mínimo."""
        pass

    def resolver(self, producto):
        """Llamado cuando el stock es repuesto y supera el mínimo.
        Implementar en subclases si aplica; por defecto no hace nada."""
        return None


class Alerta(Observador):
    """
    Observador concreto.
    Se activa cuando el stock de un Producto cae bajo el mínimo.
    Composición con Producto — no tiene sentido sin él.
    """
    def __init__(self):
        self.historial = []

    def actualizar(self, producto):
        entrada = {
            "tipo": "alerta",
            "producto": producto.nombre,
            "mensaje": f"Stock bajo en '{producto.nombre}'",
            "stock_actual": producto.stock_actual,
            "stock_minimo": producto.stock_minimo,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        self.historial.append(entrada)
        return entrada

    def resolver(self, producto):
        """Registra en el historial que el stock fue normalizado."""
        entrada = {
            "tipo": "reposicion_ok",
            "producto": producto.nombre,
            "mensaje": f"Stock normalizado en '{producto.nombre}'",
            "stock_actual": producto.stock_actual,
            "stock_minimo": producto.stock_minimo,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        self.historial.append(entrada)
        return entrada


class OrdenReposicion(Observador):
    """
    Observador concreto.
    Genera una orden de reposición automática ante stock bajo.
    """
    def __init__(self):
        self.ordenes = []

    def actualizar(self, producto):
        entrada = {
            "tipo": "orden",
            "producto": producto.nombre,
            "mensaje": f"Reponer '{producto.nombre}'",
            "cantidad_sugerida": producto.stock_minimo * 2,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "estado": "pendiente"
        }
        self.ordenes.append(entrada)
        return entrada

    def resolver(self, producto):
        """Cierra automáticamente todas las órdenes pendientes del producto repuesto."""
        ahora   = datetime.now().strftime("%d/%m/%Y %H:%M")
        cerradas = []
        for orden in self.ordenes:
            if orden["producto"] == producto.nombre and orden["estado"] == "pendiente":
                orden["estado"]            = "resuelta"
                orden["fecha_resolucion"] = ahora
                cerradas.append(orden)
        return cerradas if cerradas else None


# ─────────────────────────────────────────────────────────────
#  PATRÓN STRATEGY
#  Contexto: GeneradorReporte
#  Estrategias: ReporteReposicion, ReporteStockActual
# ─────────────────────────────────────────────────────────────

class EstrategiaReporte(ABC):
    """Interfaz base para todas las estrategias de reporte."""
    @abstractmethod
    def generar(self, productos):
        pass


class ReporteReposicion(EstrategiaReporte):
    """Estrategia: devuelve solo productos con stock bajo mínimo."""
    def generar(self, productos):
        return [
            {
                "nombre": p.nombre,
                "categoria": p.categoria,
                "stock_actual": p.stock_actual,
                "stock_minimo": p.stock_minimo,
                "precio": p.precio
            }
            for p in productos if p.stock_actual < p.stock_minimo
        ]


class ReporteStockActual(EstrategiaReporte):
    """Estrategia: devuelve todos los productos con su estado completo."""
    def generar(self, productos):
        return [
            {
                "nombre": p.nombre,
                "categoria": p.categoria,
                "stock_actual": p.stock_actual,
                "stock_minimo": p.stock_minimo,
                "precio": p.precio,
                "bajo_stock": p.stock_actual < p.stock_minimo
            }
            for p in productos
        ]


class GeneradorReporte:
    """
    Contexto del patrón Strategy.
    Delega la generación del reporte en la estrategia configurada.
    Se puede cambiar la estrategia en tiempo de ejecución.
    """
    def __init__(self, estrategia: EstrategiaReporte):
        self._estrategia = estrategia

    def cambiar_estrategia(self, estrategia: EstrategiaReporte):
        self._estrategia = estrategia

    def ejecutar(self, productos):
        return self._estrategia.generar(productos)


# ─────────────────────────────────────────────────────────────
#  CLASES DEL DOMINIO
# ─────────────────────────────────────────────────────────────

class Categoria:
    """
    Agrupa productos por rubro.
    Relación de AGREGACIÓN con Producto:
    existe aunque no tenga productos asignados.
    """
    def __init__(self, nombre, descripcion=""):
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self):
        return {"nombre": self.nombre, "descripcion": self.descripcion}


class Producto:
    """
    Entidad central del sistema.
    Sujeto del patrón Observer:
    notifica a sus observadores cuando stock_actual < stock_minimo.
    """
    _contador = 1

    def __init__(self, nombre, descripcion, precio, stock_actual, stock_minimo, categoria):
        self.id = Producto._contador
        Producto._contador += 1
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = float(precio)
        self.stock_actual = int(stock_actual)
        self.stock_minimo = int(stock_minimo)
        self.categoria = categoria
        self._observadores = []
        self.ultimas_notificaciones = []

    def agregar_observador(self, obs: Observador):
        self._observadores.append(obs)

    def _notificar(self):
        """Notifica a todos los observadores cuando el stock cae bajo el mínimo."""
        self.ultimas_notificaciones = []
        for obs in self._observadores:
            resultado = obs.actualizar(self)
            if resultado:
                self.ultimas_notificaciones.append(resultado)

    def _notificar_reposicion(self):
        """Notifica a todos los observadores cuando el stock es repuesto correctamente."""
        self.ultimas_notificaciones = []
        for obs in self._observadores:
            resultado = obs.resolver(self)
            if resultado:
                if isinstance(resultado, list):
                    self.ultimas_notificaciones.extend(resultado)
                else:
                    self.ultimas_notificaciones.append(resultado)

    def registrar_salida(self, cantidad, motivo="Sin motivo"):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        if cantidad > self.stock_actual:
            raise ValueError(f"Stock insuficiente. Stock actual: {self.stock_actual}")
        self.stock_actual -= cantidad
        mov = StockMovimiento(self.id, self.nombre, cantidad, "salida", motivo)
        if self.bajo_stock:
            self._notificar()
        else:
            self.ultimas_notificaciones = []
        return mov

    def registrar_entrada(self, cantidad, motivo="Reposición"):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        self.stock_actual += cantidad
        mov = StockMovimiento(self.id, self.nombre, cantidad, "entrada", motivo)
        if not self.bajo_stock:
            self._notificar_reposicion()
        else:
            self.ultimas_notificaciones = []
        return mov

    @property
    def bajo_stock(self):
        return self.stock_actual < self.stock_minimo

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock_actual": self.stock_actual,
            "stock_minimo": self.stock_minimo,
            "categoria": self.categoria,
            "bajo_stock": self.bajo_stock
        }


class StockMovimiento:
    """
    Registra cada entrada o salida de stock.
    Permite trazabilidad completa del inventario.
    """
    _contador = 1

    def __init__(self, producto_id, producto_nombre, cantidad, tipo, motivo):
        self.id = StockMovimiento._contador
        StockMovimiento._contador += 1
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.cantidad = cantidad
        self.tipo = tipo
        self.motivo = motivo
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "producto": self.producto_nombre,
            "cantidad": self.cantidad,
            "tipo": self.tipo,
            "motivo": self.motivo,
            "fecha": self.fecha
        }


class Empleado:
    """Actor del sistema. Registra movimientos de stock."""
    def __init__(self, nombre, apellido, legajo, rol):
        self.nombre = nombre
        self.apellido = apellido
        self.legajo = legajo
        self.rol = rol

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "legajo": self.legajo,
            "rol": self.rol
        }
```

---

## `src/app.py`

```python
"""
FerreRAP — API Flask
IS2 · UCP · 2026
"""

import io
from datetime import datetime

from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
from models import (
    Producto, Alerta, OrdenReposicion,
    GeneradorReporte, ReporteReposicion, ReporteStockActual,
)

# ── PDF ────────────────────────────────────────────────────────
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# ── Excel ──────────────────────────────────────────────────────
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ──────────────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)

USUARIOS = {
    "admin":    {"password": "admin123",    "rol": "Administrador"},
    "empleado": {"password": "empleado123", "rol": "Empleado"},
}

productos   = []
movimientos = []
alerta_obs  = Alerta()
orden_obs   = OrdenReposicion()

def seed():
    datos = [
        ("Martillo 500g",     "Martillo de carpintero",    1500, 8,  5,  "Herramientas"),
        ("Destornillador Ph", "Phillips punta fina #2",     800, 3,  5,  "Herramientas"),
        ("Cable 2.5mm x mt",  "Cable unipolar color rojo",  350, 20, 10, "Electricidad"),
        ("Llave de paso 1/2", "Bronce, media pulgada",     2200, 2,  4,  "Plomería"),
        ("Látex blanco 4L",   "Interior lavable",          3800, 12, 6,  "Pinturas"),
        ("Tornillos 4x40",    "Pack x100 unidades",         650, 50, 20, "Fijaciones"),
        ("Cinta aisladora",   "10 metros, color negro",     300, 7,  5,  "Electricidad"),
        ("Lija grano 120",    "Para madera y metal",        180, 4,  8,  "Herramientas"),
    ]
    for nombre, desc, precio, stock, minimo, cat in datos:
        p = Producto(nombre, desc, precio, stock, minimo, cat)
        p.agregar_observador(alerta_obs)
        p.agregar_observador(orden_obs)
        productos.append(p)

seed()

# ════════════════════════════════════════════════════════════
#  AUTH
# ════════════════════════════════════════════════════════════

@app.route("/api/login", methods=["POST"])
def login():
    d        = request.json or {}
    usuario  = d.get("usuario", "").strip()
    password = d.get("password", "").strip()
    u = USUARIOS.get(usuario)
    if u and u["password"] == password:
        return jsonify({"ok": True, "usuario": usuario, "rol": u["rol"]})
    return jsonify({"ok": False, "error": "Usuario o contraseña incorrectos."}), 401

# ════════════════════════════════════════════════════════════
#  FRONTEND
# ════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# ════════════════════════════════════════════════════════════
#  PRODUCTOS
# ════════════════════════════════════════════════════════════

@app.route("/api/productos", methods=["GET"])
def get_productos():
    return jsonify([p.to_dict() for p in productos])

@app.route("/api/productos", methods=["POST"])
def crear_producto():
    d       = request.json or {}
    errores = []
    if not d.get("nombre"):    errores.append("El nombre es obligatorio.")
    if not d.get("categoria"): errores.append("La categoria es obligatoria.")
    try:    float(d.get("precio", "x"))
    except: errores.append("El precio debe ser un numero.")
    try:    int(d.get("stock_actual", "x"))
    except: errores.append("El stock actual debe ser entero.")
    try:    int(d.get("stock_minimo", "x"))
    except: errores.append("El stock minimo debe ser entero.")
    if errores:
        return jsonify({"error": " | ".join(errores)}), 400
    p = Producto(d["nombre"], d.get("descripcion", ""), d["precio"],
                 d["stock_actual"], d["stock_minimo"], d["categoria"])
    p.agregar_observador(alerta_obs)
    p.agregar_observador(orden_obs)
    productos.append(p)
    return jsonify(p.to_dict()), 201

# ════════════════════════════════════════════════════════════
#  MOVIMIENTOS
# ════════════════════════════════════════════════════════════

@app.route("/api/movimientos", methods=["GET"])
def get_movimientos():
    return jsonify([m.to_dict() for m in reversed(movimientos)])

@app.route("/api/movimientos", methods=["POST"])
def registrar_movimiento():
    d = request.json or {}
    try:
        producto_id = int(d.get("producto_id", 0))
        cantidad    = int(d.get("cantidad", 0))
    except:
        return jsonify({"error": "Datos invalidos."}), 400
    tipo   = d.get("tipo", "salida")
    motivo = d.get("motivo", "Sin motivo").strip() or "Sin motivo"
    p = next((x for x in productos if x.id == producto_id), None)
    if not p:
        return jsonify({"error": "Producto no encontrado."}), 404
    try:
        mov = p.registrar_salida(cantidad, motivo) if tipo == "salida" \
              else p.registrar_entrada(cantidad, motivo)
        movimientos.append(mov)
        return jsonify({"movimiento": mov.to_dict(), "producto": p.to_dict(),
                        "notificaciones": p.ultimas_notificaciones}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# ════════════════════════════════════════════════════════════
#  ALERTAS
# ════════════════════════════════════════════════════════════

@app.route("/api/alertas", methods=["GET"])
def get_alertas():
    return jsonify(list(reversed(alerta_obs.historial)))

# ════════════════════════════════════════════════════════════
#  REPORTES — JSON (Strategy)
# ════════════════════════════════════════════════════════════

@app.route("/api/reportes/<tipo>", methods=["GET"])
def get_reporte(tipo):
    if tipo == "reposicion":
        gen = GeneradorReporte(ReporteReposicion())
    elif tipo == "stock":
        gen = GeneradorReporte(ReporteStockActual())
    else:
        return jsonify({"error": "Tipo invalido."}), 400
    return jsonify(gen.ejecutar(productos))

# ════════════════════════════════════════════════════════════
#  EXPORTAR PDF
# ════════════════════════════════════════════════════════════

@app.route("/api/reportes/<tipo>/pdf", methods=["GET"])
def exportar_pdf(tipo):
    """
    Genera y descarga un PDF del reporte indicado.
    Rutas: /api/reportes/stock/pdf  |  /api/reportes/reposicion/pdf
    """
    if tipo == "reposicion":
        gen    = GeneradorReporte(ReporteReposicion())
        titulo = "Reporte de productos a reponer"
    elif tipo == "stock":
        gen    = GeneradorReporte(ReporteStockActual())
        titulo = "Reporte de stock actual"
    else:
        return jsonify({"error": "Tipo invalido."}), 400

    datos = gen.ejecutar(productos)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=2*cm,    bottomMargin=2*cm,
    )

    styles  = getSampleStyleSheet()
    azul    = colors.HexColor("#2563eb")
    gris_hd = colors.HexColor("#1e293b")
    gris_bg = colors.HexColor("#f1f5f9")
    rojo    = colors.HexColor("#dc2626")
    verde   = colors.HexColor("#16a34a")

    estilo_titulo = ParagraphStyle(
        "titulo",
        parent=styles["Normal"],
        fontSize=18, fontName="Helvetica-Bold",
        textColor=azul, spaceAfter=4, alignment=TA_CENTER,
    )
    estilo_sub = ParagraphStyle(
        "sub",
        parent=styles["Normal"],
        fontSize=9, textColor=colors.HexColor("#6b7280"),
        alignment=TA_CENTER, spaceAfter=18,
    )

    elementos = [
        Paragraph("FerreRAP", estilo_titulo),
        Paragraph(f"{titulo} · Generado el {fecha}", estilo_sub),
    ]

    if tipo == "stock":
        cabecera = ["#", "Nombre", "Categoría", "Stock actual", "Stock mínimo", "Precio", "Estado"]
        col_w    = [1*cm, 5.5*cm, 3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm]
    else:
        cabecera = ["#", "Nombre", "Categoría", "Stock actual", "Stock mínimo", "Precio"]
        col_w    = [1*cm, 6*cm, 3.5*cm, 3*cm, 3*cm, 3*cm]

    filas = [cabecera]
    for i, p in enumerate(datos, 1):
        bajo = p.get("bajo_stock", p["stock_actual"] < p["stock_minimo"])
        fila = [
            str(i),
            p["nombre"],
            p["categoria"],
            str(p["stock_actual"]),
            str(p["stock_minimo"]),
            f"${p['precio']:,.0f}",
        ]
        if tipo == "stock":
            fila.append("⚠ Reponer" if bajo else "OK")
        filas.append(fila)

    tabla = Table(filas, colWidths=col_w, repeatRows=1)

    ts = [
        ("BACKGROUND",  (0, 0), (-1, 0), gris_hd),
        ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0), 8),
        ("ALIGN",       (0, 0), (-1, 0), "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUND", (0, 1), (-1, -1), [colors.white, gris_bg]),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 8),
        ("ALIGN",       (3, 1), (-1, -1), "CENTER"),
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]

    for i, p in enumerate(datos, 1):
        bajo = p.get("bajo_stock", p["stock_actual"] < p["stock_minimo"])
        if bajo:
            ts.append(("TEXTCOLOR", (3, i), (3, i), rojo))
            ts.append(("FONTNAME",  (3, i), (3, i), "Helvetica-Bold"))
            if tipo == "stock":
                ts.append(("TEXTCOLOR", (-1, i), (-1, i), rojo))

    tabla.setStyle(TableStyle(ts))
    elementos.append(tabla)

    total    = len(datos)
    bajo_cnt = sum(1 for p in datos if p.get("bajo_stock", p["stock_actual"] < p["stock_minimo"]))
    estilo_pie = ParagraphStyle(
        "pie", parent=styles["Normal"],
        fontSize=8, textColor=colors.HexColor("#6b7280"),
        spaceBefore=14, alignment=TA_CENTER,
    )
    elementos.append(Spacer(1, 0.4*cm))
    elementos.append(Paragraph(
        f"Total: <b>{total}</b> productos  ·  Bajo stock: <b><font color='#dc2626'>{bajo_cnt}</font></b>  ·  FerreRAP IS2 · UCP · 2026",
        estilo_pie,
    ))

    doc.build(elementos)
    buffer.seek(0)
    nombre_archivo = f"ferrerap_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    return send_file(
        buffer, mimetype="application/pdf",
        as_attachment=True, download_name=nombre_archivo,
    )

# ════════════════════════════════════════════════════════════
#  EXPORTAR EXCEL
# ════════════════════════════════════════════════════════════

@app.route("/api/reportes/<tipo>/excel", methods=["GET"])
def exportar_excel(tipo):
    """
    Genera y descarga un .xlsx del reporte indicado.
    Rutas: /api/reportes/stock/excel  |  /api/reportes/reposicion/excel
    """
    if tipo == "reposicion":
        gen    = GeneradorReporte(ReporteReposicion())
        titulo = "Productos a reponer"
    elif tipo == "stock":
        gen    = GeneradorReporte(ReporteStockActual())
        titulo = "Stock actual"
    else:
        return jsonify({"error": "Tipo invalido."}), 400

    datos = gen.ejecutar(productos)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = titulo[:31]

    azul_hd   = "1E3A5F"
    azul_sub  = "2563EB"
    gris_par  = "F1F5F9"
    rojo_hex  = "DC2626"
    verde_hex = "16A34A"
    blanco    = "FFFFFF"

    thin = Side(style="thin", color="D1D5DB")
    borde_all = Border(left=thin, right=thin, top=thin, bottom=thin)

    ws.merge_cells("A1:G1")
    c = ws["A1"]
    c.value     = "FerreRAP — Sistema de Gestión de Stock"
    c.font      = Font(bold=True, size=16, color=blanco, name="Calibri")
    c.fill      = PatternFill("solid", fgColor=azul_hd)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    ws.merge_cells("A2:G2")
    c = ws["A2"]
    c.value     = f"{titulo}  ·  Generado el {fecha}  ·  IS2 · UCP · 2026"
    c.font      = Font(size=9, color="6B7280", italic=True, name="Calibri")
    c.fill      = PatternFill("solid", fgColor="EFF6FF")
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 18

    ws.append([])

    if tipo == "stock":
        cabecera = ["#", "Nombre", "Descripción", "Categoría", "Stock actual", "Stock mínimo", "Precio ($)", "Estado"]
        anchos   = [5, 24, 28, 14, 13, 13, 12, 10]
    else:
        cabecera = ["#", "Nombre", "Descripción", "Categoría", "Stock actual", "Stock mínimo", "Precio ($)"]
        anchos   = [5, 24, 28, 14, 13, 13, 12]

    fila_hd = ws.max_row + 1
    ws.append(cabecera)
    for col_i, val in enumerate(cabecera, 1):
        c = ws.cell(row=fila_hd, column=col_i)
        c.font      = Font(bold=True, color=blanco, size=10, name="Calibri")
        c.fill      = PatternFill("solid", fgColor=azul_sub)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border    = borde_all
    ws.row_dimensions[fila_hd].height = 20

    for i, p in enumerate(datos, 1):
        bajo = p.get("bajo_stock", p["stock_actual"] < p["stock_minimo"])
        fila = [
            i,
            p["nombre"],
            p.get("descripcion", ""),
            p["categoria"],
            p["stock_actual"],
            p["stock_minimo"],
            p["precio"],
        ]
        if tipo == "stock":
            fila.append("⚠ Reponer" if bajo else "OK")

        fila_n = ws.max_row + 1
        ws.append(fila)
        bg = gris_par if i % 2 == 0 else blanco

        for col_i, _ in enumerate(fila, 1):
            c = ws.cell(row=fila_n, column=col_i)
            c.fill   = PatternFill("solid", fgColor=bg)
            c.border = borde_all
            c.font   = Font(size=10, name="Calibri")

            if col_i == 5 and bajo:
                c.font = Font(bold=True, color=rojo_hex, size=10, name="Calibri")
            if tipo == "stock" and col_i == 8:
                c.alignment = Alignment(horizontal="center")
                if bajo:
                    c.font = Font(bold=True, color=rojo_hex, size=10, name="Calibri")
                else:
                    c.font = Font(bold=True, color=verde_hex, size=10, name="Calibri")
            if col_i == 7:
                c.number_format = '#,##0.00'
                c.alignment     = Alignment(horizontal="right")
            if col_i in (1, 4, 5, 6):
                c.alignment = Alignment(horizontal="center")

        ws.row_dimensions[fila_n].height = 17

    for col_i, ancho in enumerate(anchos, 1):
        ws.column_dimensions[get_column_letter(col_i)].width = ancho

    ws.append([])
    fila_tot = ws.max_row + 1
    total    = len(datos)
    bajo_cnt = sum(1 for p in datos if p.get("bajo_stock", p["stock_actual"] < p["stock_minimo"]))

    ws.merge_cells(f"A{fila_tot}:G{fila_tot}" if tipo != "stock" else f"A{fila_tot}:H{fila_tot}")
    c = ws.cell(row=fila_tot, column=1)
    c.value     = f"Total: {total} productos  |  Bajo stock: {bajo_cnt}  |  FerreRAP IS2 · UCP · 2026"
    c.font      = Font(italic=True, size=9, color="6B7280", name="Calibri")
    c.alignment = Alignment(horizontal="center")

    ws.freeze_panes = ws.cell(row=fila_hd + 1, column=1)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    nombre_archivo = f"ferrerap_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    return send_file(
        buffer,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=nombre_archivo,
    )

# ════════════════════════════════════════════════════════════
#  STATS
# ════════════════════════════════════════════════════════════

@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify({
        "total_productos":   len(productos),
        "bajo_stock":        sum(1 for p in productos if p.bajo_stock),
        "total_alertas":     len(alerta_obs.historial),
        "total_movimientos": len(movimientos),
    })

if __name__ == "__main__":
    print("\n  FerreRAP — IS2 · UCP · 2026")
    print("  http://localhost:5000")
    print("  admin / admin123  |  empleado / empleado123\n")
    app.run(debug=True, port=5000)
```

---

## `src/index.html` — Resumen de secciones (SPA, 1303 líneas)

La SPA está compuesta por las siguientes secciones lógicas:

| Sección          | ID HTML          | Descripción                                               |
|------------------|------------------|-----------------------------------------------------------|
| Login            | `pantalla-login` | Formulario con credenciales, validación client-side       |
| App principal    | `pantalla-app`   | Header + Nav + Main                                       |
| Inventario       | `#inventario`    | Stats cards + tabla con buscador filtrable                |
| Movimientos      | `#movimientos`   | Formulario entrada/salida + feed historial (Observer UI)  |
| Alertas          | `#alertas`       | Feed de alertas + lista de productos críticos             |
| Reportes         | `#reportes`      | Selector Strategy + export PDF/Excel                      |
| Nuevo producto   | `#nuevo`         | Formulario CRUD (solo Administrador)                      |

### Variables CSS (design tokens)

```css
:root {
  --bg, --surface, --surface2, --border, --border2
  --azul, --azul-l, --azul-btn, --azul-h
  --verde, --verde-l, --rojo, --rojo-l, --naranja, --naranja-l
  --texto, --muted, --muted2
  --shadow, --shadow-md, --radius, --mono, --sans
}
/* Soporte dark mode completo via [data-theme="dark"] */
```

### Endpoints consumidos desde el frontend

| Método | Ruta                              | Función JS               |
|--------|-----------------------------------|--------------------------|
| POST   | `/api/login`                      | `hacerLogin()`           |
| GET    | `/api/stats`                      | `cargarStats()`          |
| GET    | `/api/productos`                  | `cargarProductos()`      |
| POST   | `/api/productos`                  | `crearProducto()`        |
| GET    | `/api/movimientos`                | `cargarMovimientos()`    |
| POST   | `/api/movimientos`                | `registrarMovimiento()`  |
| GET    | `/api/alertas`                    | `cargarAlertas()`        |
| GET    | `/api/reportes/{tipo}`            | `cargarReporte(tipo)`    |
| GET    | `/api/reportes/{tipo}/pdf`        | `exportarReporte('pdf')` |
| GET    | `/api/reportes/{tipo}/excel`      | `exportarReporte('excel')`|

---

## `docs/AI_LOG.md` — Resumen de entradas

| Entrada | Herramienta | Responsable      | Uso                                              |
|---------|-------------|------------------|--------------------------------------------------|
| 001     | ChatGPT     | Dev Lead         | Tabla de integrantes y roles                     |
| 002     | ChatGPT     | Dev Lead         | Estructura del repositorio GitHub                |
| 003     | ChatGPT     | Scrum / Dev Lead | Gestión de colaboradores GitHub                  |
| 004     | ChatGPT     | Scrum / Dev Lead | Estrategias Matriz de Riesgos                    |
| 005     | ChatGPT     | Dev Lead         | Código Mermaid — diagrama de clases              |
| 006     | Claude      | Scrum Master     | División de tareas para el Kanban                |
| 007     | Claude      | —                | Prototipo navegable HTML/CSS/JS (5 pantallas)    |
| 008     | Gemini      | QA Lead          | Patrón Strategy para exportación de reportes     |
| 009     | Claude      | Scrum Master     | División TP1 en tarjetas Kanban                  |
| 010     | Claude      | Scrum Master     | Redacción `docs/patrones-tp1.md`                 |

---

## API endpoints — Resumen completo

| Método | Ruta                          | Auth | Descripción                        |
|--------|-------------------------------|------|------------------------------------|
| POST   | `/api/login`                  | —    | Autenticación básica               |
| GET    | `/api/productos`              | —    | Lista completa de productos        |
| POST   | `/api/productos`              | —    | Crear producto (valida campos)     |
| GET    | `/api/movimientos`            | —    | Historial de movimientos (rev.)    |
| POST   | `/api/movimientos`            | —    | Registrar entrada o salida         |
| GET    | `/api/alertas`                | —    | Historial de alertas Observer      |
| GET    | `/api/reportes/stock`         | —    | Reporte JSON stock completo        |
| GET    | `/api/reportes/reposicion`    | —    | Reporte JSON solo bajo stock       |
| GET    | `/api/reportes/stock/pdf`     | —    | Descarga PDF stock (reportlab)     |
| GET    | `/api/reportes/reposicion/pdf`| —    | Descarga PDF reposición            |
| GET    | `/api/reportes/stock/excel`   | —    | Descarga .xlsx stock (openpyxl)    |
| GET    | `/api/reportes/reposicion/excel`| —  | Descarga .xlsx reposición          |
| GET    | `/api/stats`                  | —    | Conteos globales del sistema       |
| GET    | `/`                           | —    | Sirve `index.html`                 |

---

## Datos de seed (inicial)

| Nombre              | Descripción                  | Precio | Stock | Mínimo | Categoría    |
|---------------------|------------------------------|--------|-------|--------|--------------|
| Martillo 500g       | Martillo de carpintero       | 1500   | 8     | 5      | Herramientas |
| Destornillador Ph   | Phillips punta fina #2       | 800    | 3     | 5      | Herramientas |
| Cable 2.5mm x mt    | Cable unipolar color rojo    | 350    | 20    | 10     | Electricidad |
| Llave de paso 1/2   | Bronce, media pulgada        | 2200   | 2     | 4      | Plomería     |
| Látex blanco 4L     | Interior lavable             | 3800   | 12    | 6      | Pinturas     |
| Tornillos 4x40      | Pack x100 unidades           | 650    | 50    | 20     | Fijaciones   |
| Cinta aisladora     | 10 metros, color negro       | 300    | 7     | 5      | Electricidad |
| Lija grano 120      | Para madera y metal          | 180    | 4     | 8      | Herramientas |

> ⚠ Productos con stock bajo mínimo desde el inicio: Destornillador Ph (3/5), Llave de paso 1/2 (2/4), Lija grano 120 (4/8)

---

## Usuarios del sistema

| Usuario   | Contraseña    | Rol            | Permisos                          |
|-----------|---------------|----------------|-----------------------------------|
| `admin`   | `admin123`    | Administrador  | Todas las secciones + crear productos |
| `empleado`| `empleado123` | Empleado       | Inventario, Movimientos, Alertas, Reportes |
