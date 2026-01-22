import { Routes } from '@angular/router';
import { INVENTARIO_ROUTES } from './inventario/inventario.routes';

export const routes: Routes = [
  { path: 'inventario', children: INVENTARIO_ROUTES },
  { path: '', pathMatch: 'full', redirectTo: 'inventario' },
];
