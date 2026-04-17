-- ═══════════════════════════════════════════════════════
--  FerreRAP — Setup de Base de Datos (Supabase)
--  IS2 · UCP · 2026
--  Ejecutar en: Supabase Dashboard → SQL Editor
-- ═══════════════════════════════════════════════════════

-- Productos
CREATE TABLE IF NOT EXISTS productos (
  id BIGSERIAL PRIMARY KEY,
  nombre TEXT NOT NULL,
  descripcion TEXT DEFAULT '',
  precio_costo NUMERIC(12,2) NOT NULL DEFAULT 0,
  precio_venta NUMERIC(12,2) NOT NULL DEFAULT 0,
  stock_actual INTEGER NOT NULL DEFAULT 0,
  stock_minimo INTEGER NOT NULL DEFAULT 1,
  categoria TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Movimientos de stock
CREATE TABLE IF NOT EXISTS movimientos (
  id BIGSERIAL PRIMARY KEY,
  producto_id BIGINT REFERENCES productos(id),
  producto_nombre TEXT NOT NULL,
  cantidad INTEGER NOT NULL,
  tipo TEXT NOT NULL CHECK (tipo IN ('entrada','salida')),
  motivo TEXT DEFAULT 'Sin motivo',
  precio_unitario NUMERIC(12,2) DEFAULT 0,
  total NUMERIC(12,2) DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Alertas (Patrón Observer)
CREATE TABLE IF NOT EXISTS alertas (
  id BIGSERIAL PRIMARY KEY,
  producto_nombre TEXT NOT NULL,
  mensaje TEXT NOT NULL,
  tipo TEXT NOT NULL DEFAULT 'alerta',
  stock_actual INTEGER NOT NULL,
  stock_minimo INTEGER NOT NULL,
  leida BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Órdenes de reposición (Patrón Observer)
CREATE TABLE IF NOT EXISTS ordenes_reposicion (
  id BIGSERIAL PRIMARY KEY,
  producto_nombre TEXT NOT NULL,
  mensaje TEXT NOT NULL,
  cantidad_sugerida INTEGER NOT NULL,
  estado TEXT DEFAULT 'pendiente',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  fecha_resolucion TIMESTAMPTZ
);

-- Ventas (carrito confirmado)
CREATE TABLE IF NOT EXISTS ventas (
  id BIGSERIAL PRIMARY KEY,
  usuario TEXT NOT NULL,
  total NUMERIC(12,2) NOT NULL DEFAULT 0,
  items_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Items de cada venta
CREATE TABLE IF NOT EXISTS venta_items (
  id BIGSERIAL PRIMARY KEY,
  venta_id BIGINT REFERENCES ventas(id),
  producto_id BIGINT REFERENCES productos(id),
  producto_nombre TEXT NOT NULL,
  cantidad INTEGER NOT NULL,
  precio_unitario NUMERIC(12,2) NOT NULL,
  subtotal NUMERIC(12,2) NOT NULL
);

-- ═══════════════════════════════════════════════════════
--  RLS — Permitir acceso con clave anon
-- ═══════════════════════════════════════════════════════

ALTER TABLE productos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_all_productos" ON productos FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE movimientos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_all_movimientos" ON movimientos FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE alertas ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_all_alertas" ON alertas FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE ordenes_reposicion ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_all_ordenes" ON ordenes_reposicion FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE ventas ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_all_ventas" ON ventas FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE venta_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_all_venta_items" ON venta_items FOR ALL USING (true) WITH CHECK (true);

-- ═══════════════════════════════════════════════════════
--  NUEVAS COLUMNAS — Método de Pago + Facturación
--  Ejecutar en Supabase SQL Editor si ya tenés la tabla creada
-- ═══════════════════════════════════════════════════════
ALTER TABLE ventas ADD COLUMN IF NOT EXISTS metodo_pago TEXT DEFAULT 'efectivo';
ALTER TABLE ventas ADD COLUMN IF NOT EXISTS factura_tipo TEXT;
ALTER TABLE ventas ADD COLUMN IF NOT EXISTS factura_situacion TEXT;
ALTER TABLE ventas ADD COLUMN IF NOT EXISTS factura_nombre TEXT;
ALTER TABLE ventas ADD COLUMN IF NOT EXISTS factura_dni TEXT;
ALTER TABLE ventas ADD COLUMN IF NOT EXISTS factura_cuit TEXT;
ALTER TABLE ventas ADD COLUMN IF NOT EXISTS factura_direccion TEXT;
