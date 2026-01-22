from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

class TimeStampedModel(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Categoria(TimeStampedModel):
    nombre = models.CharField(max_length=120, unique=True)
    padre = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="hijos")  # categoría padre
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Marca(TimeStampedModel):
    nombre = models.CharField(max_length=120, unique=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class UnidadMedida(TimeStampedModel):
    nombre = models.CharField(max_length=120, unique=True)
    simbolo = models.CharField(max_length=20, blank=True, default="")  # ej: kg, un, L
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.simbolo})" if self.simbolo else self.nombre

class Proveedor(TimeStampedModel):
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=20, blank=True, default="")
    telefono = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    direccion = models.CharField(max_length=255, blank=True, default="")
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = [("nombre", "rut")]
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Producto(TimeStampedModel):
    sku = models.CharField(max_length=60, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default="")
    codigo_barra = models.CharField(max_length=80, blank=True, default="")

    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, null=True, blank=True, related_name="productos")
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name="productos")

    categorias = models.ManyToManyField(Categoria, blank=True, related_name="productos")  # múltiples categorías

    activo = models.BooleanField(default=True)
    permite_fraccion = models.BooleanField(default=True)  # permite decimales en cantidades
    stock_minimo = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    stock_maximo = models.DecimalField(max_digits=14, decimal_places=3, default=0)

    costo_promedio = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    precio_referencia = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    ubicacion = models.CharField(max_length=120, blank=True, default="")  # rack/pasillo/estante

    class Meta:
        ordering = ["nombre"]
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["nombre"]),
            models.Index(fields=["codigo_barra"]),
        ]

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

class ProductoProveedor(TimeStampedModel):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="proveedores")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name="productos")

    codigo_proveedor = models.CharField(max_length=80, blank=True, default="")
    costo_ultima_compra = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    costo_referencia = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    es_principal = models.BooleanField(default=False)

    class Meta:
        unique_together = [("producto", "proveedor")]
        ordering = ["-es_principal", "proveedor__nombre"]

    def __str__(self):
        return f"{self.producto.sku} -> {self.proveedor.nombre}"

class Bodega(TimeStampedModel):
    nombre = models.CharField(max_length=120, unique=True)
    direccion = models.CharField(max_length=255, blank=True, default="")
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Stock(TimeStampedModel):
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name="stocks")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="stocks")
    cantidad = models.DecimalField(max_digits=14, decimal_places=3, default=0)

    class Meta:
        unique_together = [("bodega", "producto")]
        indexes = [models.Index(fields=["bodega", "producto"])]
        constraints = [
            models.CheckConstraint(condition=Q(cantidad__gte=0), name="stock_no_negativo"),

        ]

    def __str__(self):
        return f"{self.bodega} | {self.producto.sku} = {self.cantidad}"


class BaseMovimiento(TimeStampedModel):
    class Estado(models.TextChoices):
        BORRADOR = "BORRADOR", "Borrador"
        POSTEADO = "POSTEADO", "Posteado"

    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.BORRADOR)
    fecha = models.DateTimeField(default=timezone.now)
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name="%(class)s_movimientos")

    referencia = models.CharField(max_length=120, blank=True, default="")  # OC/Factura/etc
    observacion = models.TextField(blank=True, default="")

    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    posteado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-fecha", "-id"]

    def clean(self):
        if not self.bodega_id:
            raise ValidationError("Debe seleccionar una bodega.")

    def _lineas(self):
        return list(self.lineas.all())

    def _validar_lineas(self):
        lineas = self._lineas()
        if not lineas:
            raise ValidationError("No puedes postear un movimiento sin líneas.")
        for l in lineas:
            if l.cantidad <= 0:
                raise ValidationError("Todas las líneas deben tener cantidad > 0.")
        return lineas

    def _get_or_create_stock_map(self, productos_ids):
        stocks = Stock.objects.select_for_update().filter(bodega_id=self.bodega_id, producto_id__in=productos_ids)
        return {(s.bodega_id, s.producto_id): s for s in stocks}  # mapa stock

    def _get_or_create_stock(self, stock_map, producto_id):
        key = (self.bodega_id, producto_id)
        if key in stock_map:
            return stock_map[key]
        s = Stock.objects.create(bodega_id=self.bodega_id, producto_id=producto_id, cantidad=0)
        stock_map[key] = s
        return s

class MovimientoEntrada(BaseMovimiento):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True, blank=True, related_name="entradas")  # proveedor opcional

    @transaction.atomic
    def postear(self):
        if self.estado != self.Estado.BORRADOR:
            raise ValidationError("Solo se pueden postear movimientos en BORRADOR.")

        lineas = self._validar_lineas()
        productos_ids = [l.producto_id for l in lineas]
        stock_map = self._get_or_create_stock_map(productos_ids)

        for l in lineas:
            st = self._get_or_create_stock(stock_map, l.producto_id)
            st.cantidad += l.cantidad
            st.save()

        self.estado = self.Estado.POSTEADO
        self.posteado_en = timezone.now()
        self.save()

class MovimientoSalida(BaseMovimiento):
    destino = models.CharField(max_length=120, blank=True, default="")

    @transaction.atomic
    def postear(self):
        if self.estado != self.Estado.BORRADOR:
            raise ValidationError("Solo se pueden postear movimientos en BORRADOR.")

        lineas = self._validar_lineas()
        productos_ids = [l.producto_id for l in lineas]
        stock_map = self._get_or_create_stock_map(productos_ids)

        for l in lineas:
            st = self._get_or_create_stock(stock_map, l.producto_id)
            if st.cantidad < l.cantidad:
                raise ValidationError(
                    f"Stock insuficiente para {l.producto.sku}. Disponible: {st.cantidad}, solicitado: {l.cantidad}"
                )
            st.cantidad -= l.cantidad
            st.save()

        self.estado = self.Estado.POSTEADO
        self.posteado_en = timezone.now()
        self.save()

class MovimientoLinea(TimeStampedModel):
    movimiento_entrada = models.ForeignKey(
        MovimientoEntrada, on_delete=models.CASCADE, related_name="lineas", null=True, blank=True
    )
    movimiento_salida = models.ForeignKey(
        MovimientoSalida, on_delete=models.CASCADE, related_name="lineas", null=True, blank=True
    )

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="lineas_movimiento")
    cantidad = models.DecimalField(max_digits=14, decimal_places=3)
    costo_unitario = models.DecimalField(max_digits=14, decimal_places=2, default=0)  # útil en entradas

    lote = models.CharField(max_length=80, blank=True, default="")
    vencimiento = models.DateField(null=True, blank=True)
    observacion = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    (Q(movimiento_entrada__isnull=False) & Q(movimiento_salida__isnull=True)) |
                    (Q(movimiento_entrada__isnull=True) & Q(movimiento_salida__isnull=False))
                ),
                name="linea_xor_entrada_salida"
            )
        ]
        indexes = [
            models.Index(fields=["producto"]),
        ]

    def __str__(self):
        return f"{self.producto.sku} x {self.cantidad}"

    def clean(self):
        if self.cantidad is None or self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")

        if self.producto_id and not self.producto.permite_fraccion:
            if self.cantidad != self.cantidad.to_integral_value():
                raise ValidationError(f"El producto {self.producto.sku} no permite fracciones.")
