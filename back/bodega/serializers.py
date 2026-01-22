from rest_framework import serializers
from django.db import transaction
from .models import *

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "padre", "activa", "creado_en", "actualizado_en"]

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ["id", "nombre", "activa", "creado_en", "actualizado_en"]

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = ["id", "nombre", "simbolo", "activa", "creado_en", "actualizado_en"]

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = [
            "id", "nombre", "rut", "telefono", "email", "direccion", "activo",
            "creado_en", "actualizado_en"
        ]

class ProductoProveedorSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source="proveedor.nombre", read_only=True)

    class Meta:
        model = ProductoProveedor
        fields = [
            "id",
            "producto", "proveedor", "proveedor_nombre",
            "codigo_proveedor",
            "costo_ultima_compra", "costo_referencia",
            "es_principal",
            "creado_en", "actualizado_en"
        ]

class ProductoSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.CharField(source="marca.nombre", read_only=True)
    unidad_medida_nombre = serializers.CharField(source="unidad_medida.nombre", read_only=True)
    categorias_detalle = CategoriaSerializer(source="categorias", many=True, read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id",
            "sku", "nombre", "descripcion", "codigo_barra",
            "marca", "marca_nombre",
            "unidad_medida", "unidad_medida_nombre",
            "categorias", "categorias_detalle",
            "activo", "permite_fraccion",
            "stock_minimo", "stock_maximo",
            "costo_promedio", "precio_referencia",
            "ubicacion",
            "creado_en", "actualizado_en"
        ]

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = ["id", "nombre", "direccion", "activa", "creado_en", "actualizado_en"]

class StockSerializer(serializers.ModelSerializer):
    producto_sku = serializers.CharField(source="producto.sku", read_only=True)
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    bodega_nombre = serializers.CharField(source="bodega.nombre", read_only=True)

    class Meta:
        model = Stock
        fields = [
            "id",
            "bodega", "bodega_nombre",
            "producto", "producto_sku", "producto_nombre",
            "cantidad",
            "creado_en", "actualizado_en"
        ]

class MovimientoLineaEntradaSerializer(serializers.ModelSerializer):
    producto_sku = serializers.CharField(source="producto.sku", read_only=True)
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)

    class Meta:
        model = MovimientoLinea
        fields = [
            "id",
            "producto", "producto_sku", "producto_nombre",
            "cantidad", "costo_unitario",
            "lote", "vencimiento", "observacion",
            "creado_en", "actualizado_en"
        ]

class MovimientoLineaSalidaSerializer(serializers.ModelSerializer):
    producto_sku = serializers.CharField(source="producto.sku", read_only=True)
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)

    class Meta:
        model = MovimientoLinea
        fields = [
            "id",
            "producto", "producto_sku", "producto_nombre",
            "cantidad",
            "lote", "vencimiento", "observacion",
            "creado_en", "actualizado_en"
        ]

class MovimientoEntradaSerializer(serializers.ModelSerializer):
    lineas = MovimientoLineaEntradaSerializer(many=True, required=False)
    bodega_nombre = serializers.CharField(source="bodega.nombre", read_only=True)
    proveedor_nombre = serializers.CharField(source="proveedor.nombre", read_only=True)

    class Meta:
        model = MovimientoEntrada
        fields = [
            "id",
            "estado", "fecha",
            "bodega", "bodega_nombre",
            "proveedor", "proveedor_nombre",
            "referencia", "observacion",
            "creado_por", "posteado_en",
            "lineas",
            "creado_en", "actualizado_en"
        ]
        read_only_fields = ["creado_por", "posteado_en"]

    def validate(self, data):
        # Evitar que editen un movimiento ya posteado
        instance = getattr(self, "instance", None)
        if instance and instance.estado == MovimientoEntrada.Estado.POSTEADO:
            raise serializers.ValidationError("No puedes modificar un movimiento ya POSTEADO.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        lineas_data = validated_data.pop("lineas", [])
        request = self.context.get("request")

        movimiento = MovimientoEntrada.objects.create(
            creado_por=request.user if request and request.user.is_authenticated else None,
            **validated_data
        )

        for l in lineas_data:
            MovimientoLinea.objects.create(movimiento_entrada=movimiento, **l)

        return movimiento

    @transaction.atomic
    def update(self, instance, validated_data):
        lineas_data = validated_data.pop("lineas", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Si mandan "lineas", reemplazamos todas (modo simple)
        if lineas_data is not None:
            instance.lineas.all().delete()
            for l in lineas_data:
                MovimientoLinea.objects.create(movimiento_entrada=instance, **l)

        return instance

class MovimientoSalidaSerializer(serializers.ModelSerializer):
    lineas = MovimientoLineaSalidaSerializer(many=True, required=False)
    bodega_nombre = serializers.CharField(source="bodega.nombre", read_only=True)

    class Meta:
        model = MovimientoSalida
        fields = [
            "id",
            "estado", "fecha",
            "bodega", "bodega_nombre",
            "destino",
            "referencia", "observacion",
            "creado_por", "posteado_en",
            "lineas",
            "creado_en", "actualizado_en"
        ]
        read_only_fields = ["creado_por", "posteado_en"]

    def validate(self, data):
        instance = getattr(self, "instance", None)
        if instance and instance.estado == MovimientoSalida.Estado.POSTEADO:
            raise serializers.ValidationError("No puedes modificar un movimiento ya POSTEADO.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        lineas_data = validated_data.pop("lineas", [])
        request = self.context.get("request")

        movimiento = MovimientoSalida.objects.create(
            creado_por=request.user if request and request.user.is_authenticated else None,
            **validated_data
        )

        for l in lineas_data:
            MovimientoLinea.objects.create(movimiento_salida=movimiento, **l)

        return movimiento

    @transaction.atomic
    def update(self, instance, validated_data):
        lineas_data = validated_data.pop("lineas", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if lineas_data is not None:
            instance.lineas.all().delete()
            for l in lineas_data:
                MovimientoLinea.objects.create(movimiento_salida=instance, **l)

        return instance
