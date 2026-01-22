from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # permission_classes = [IsAuthenticated]

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    # permission_classes = [IsAuthenticated]

class UnidadMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer
    # permission_classes = [IsAuthenticated]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    # permission_classes = [IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.prefetch_related("categorias").select_related("marca", "unidad_medida")
    serializer_class = ProductoSerializer
    # permission_classes = [IsAuthenticated]

class ProductoProveedorViewSet(viewsets.ModelViewSet):
    queryset = ProductoProveedor.objects.select_related("producto", "proveedor")
    serializer_class = ProductoProveedorSerializer
    # permission_classes = [IsAuthenticated]

class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer
    # permission_classes = [IsAuthenticated]

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.select_related("bodega", "producto")
    serializer_class = StockSerializer
    # permission_classes = [IsAuthenticated]

class MovimientoEntradaViewSet(viewsets.ModelViewSet):
    queryset = MovimientoEntrada.objects.select_related("bodega", "proveedor", "creado_por").prefetch_related("lineas")
    serializer_class = MovimientoEntradaSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def postear(self, request, pk=None):
        movimiento = self.get_object()

        try:
            movimiento.postear()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(movimiento)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MovimientoSalidaViewSet(viewsets.ModelViewSet):
    queryset = MovimientoSalida.objects.select_related("bodega", "creado_por").prefetch_related("lineas")
    serializer_class = MovimientoSalidaSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def postear(self, request, pk=None):
        movimiento = self.get_object()

        try:
            movimiento.postear()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(movimiento)
        return Response(serializer.data, status=status.HTTP_200_OK)
