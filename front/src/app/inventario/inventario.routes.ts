import { Routes } from '@angular/router';
import { InventarioComponent } from './inventario.component';
import { ProductosPageComponent } from '../pages/productos-page.component';
import { BodegasPageComponent } from '../pages/bodegas-page.component';
import { StockPageComponent } from '../pages/stock-page.component';
import { MovimientosEntradaPageComponent } from '../pages/movimientos-entrada-page.component';
import { MovimientosSalidaPageComponent } from '../pages/movimientos-salida-page.component';

export const INVENTARIO_ROUTES: Routes = [
    {
        path: '',
        component: InventarioComponent,
        children: [
            { path: 'productos', component: ProductosPageComponent },
            { path: 'bodegas', component: BodegasPageComponent },
            { path: 'stock', component: StockPageComponent },
            { path: 'mov-entrada', component: MovimientosEntradaPageComponent },
            { path: 'mov-salida', component: MovimientosSalidaPageComponent },
            { path: '', pathMatch: 'full', redirectTo: 'productos' },
        ],
    },
];
