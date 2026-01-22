from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"categorias", CategoriaViewSet)
router.register(r"marcas", MarcaViewSet)
router.register(r"unidades-medida", UnidadMedidaViewSet)
router.register(r"proveedores", ProveedorViewSet)
router.register(r"productos", ProductoViewSet)
router.register(r"producto-proveedores", ProductoProveedorViewSet)
router.register(r"bodegas", BodegaViewSet)
router.register(r"stocks", StockViewSet)
router.register(r"movimientos-entrada", MovimientoEntradaViewSet)
router.register(r"movimientos-salida", MovimientoSalidaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
