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
                # resolver() puede devolver una lista (varias órdenes cerradas) o un dict
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
        # Notificar siempre que el stock esté por debajo del mínimo:
        # tanto si acaba de cruzar el umbral como si ya estaba bajo y cae más.
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
            # Stock repuesto: cerrar órdenes pendientes y registrar normalización
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
