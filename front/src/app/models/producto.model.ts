export interface Producto {
  id: number;
  sku: string;
  nombre: string;
  descripcion: string;
  codigo_barra: string;

  marca: number | null;
  marca_nombre?: string;

  unidad_medida: number;
  unidad_medida_nombre?: string;

  categorias: number[];

  activo: boolean;
  permite_fraccion: boolean;

  stock_minimo: string;
  stock_maximo: string;

  costo_promedio: string;
  precio_referencia: string;

  ubicacion: string;
}
