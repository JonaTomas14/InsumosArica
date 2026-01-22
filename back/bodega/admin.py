from django.contrib import admin
from .models import (
    Categoria, Marca, UnidadMedida, Proveedor,
    Producto, ProductoProveedor,
    Bodega, Stock,
    MovimientoEntrada, MovimientoSalida, MovimientoLinea
)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "padre", "activa", "creado_en")
    list_filter = ("activa",)
    search_fields = ("nombre",)
    autocomplete_fields = ("padre",)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "activa", "creado_en")
    list_filter = ("activa",)
    search_fields = ("nombre",)


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "simbolo", "activa", "creado_en")
    list_filter = ("activa",)
    search_fields = ("nombre", "simbolo")

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "rut", "telefono", "email", "activo", "creado_en")
    list_filter = ("activo",)
    search_fields = ("nombre", "rut", "telefono", "email")

class ProductoProveedorInline(admin.TabularInline):
    model = ProductoProveedor
    extra = 0
    autocomplete_fields = ("proveedor",)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "nombre", "marca", "unidad_medida", "activo", "creado_en")
    list_filter = ("activo", "marca", "unidad_medida")
    search_fields = ("sku", "nombre", "codigo_barra")
    autocomplete_fields = ("marca", "unidad_medida", "categorias")
    filter_horizontal = ("categorias",)
    inlines = [ProductoProveedorInline]


@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "proveedor", "codigo_proveedor", "es_principal", "costo_ultima_compra")
    list_filter = ("es_principal", "proveedor")
    search_fields = ("producto__sku", "producto__nombre", "proveedor__nombre", "codigo_proveedor")
    autocomplete_fields = ("producto", "proveedor")


# =========================
# Bodega / Stock
# =========================

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "direccion", "activa", "creado_en")
    list_filter = ("activa",)
    search_fields = ("nombre", "direccion")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "bodega", "producto", "cantidad", "actualizado_en")
    list_filter = ("bodega",)
    search_fields = ("producto__sku", "producto__nombre", "bodega__nombre")
    autocomplete_fields = ("bodega", "producto")

class MovimientoLineaEntradaInline(admin.TabularInline):
    model = MovimientoLinea
    extra = 0
    autocomplete_fields = ("producto",)

    # Solo se verá en MovimientoEntrada
    fk_name = "movimiento_entrada"


class MovimientoLineaSalidaInline(admin.TabularInline):
    model = MovimientoLinea
    extra = 0
    autocomplete_fields = ("producto",)

    # Solo se verá en MovimientoSalida
    fk_name = "movimiento_salida"


@admin.register(MovimientoEntrada)
class MovimientoEntradaAdmin(admin.ModelAdmin):
    list_display = ("id", "estado", "fecha", "bodega", "proveedor", "referencia", "posteado_en")
    list_filter = ("estado", "bodega", "proveedor")
    search_fields = ("referencia", "observacion", "proveedor__nombre")
    autocomplete_fields = ("bodega", "proveedor", "creado_por")
    inlines = [MovimientoLineaEntradaInline]


@admin.register(MovimientoSalida)
class MovimientoSalidaAdmin(admin.ModelAdmin):
    list_display = ("id", "estado", "fecha", "bodega", "destino", "referencia", "posteado_en")
    list_filter = ("estado", "bodega")
    search_fields = ("referencia", "observacion", "destino")
    autocomplete_fields = ("bodega", "creado_por")
    inlines = [MovimientoLineaSalidaInline]


@admin.register(MovimientoLinea)
class MovimientoLineaAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "cantidad", "movimiento_entrada", "movimiento_salida", "creado_en")
    search_fields = ("producto__sku", "producto__nombre", "lote")
    autocomplete_fields = ("producto", "movimiento_entrada", "movimiento_salida")
