import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-inventario',
  imports: [RouterModule],
  template: `
    <h2>Inventario</h2>

    <nav style="display:flex; gap:10px; margin-bottom:16px;">
      <a routerLink="productos">Productos</a>
      <a routerLink="bodegas">Bodegas</a>
      <a routerLink="stock">Stock</a>
      <a routerLink="mov-entrada">Mov. Entrada</a>
      <a routerLink="mov-salida">Mov. Salida</a>
    </nav>

    <router-outlet></router-outlet>
  `,
})
export class InventarioComponent {}
