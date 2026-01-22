import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductosService } from '../services/productos.service';
import { Producto } from '../models/producto.model';

@Component({
    standalone: true,
    imports: [CommonModule],
    template: `
    <h3>Productos</h3>

    <button (click)="cargar()">Recargar</button>

    <table border="1" width="100%" style="margin-top:12px;">
      <thead>
        <tr>
          <th>SKU</th>
          <th>Nombre</th>
          <th>Unidad</th>
          <th>Marca</th>
          <th>Activo</th>
          <th>Acción</th>
        </tr>
      </thead>

      <tbody>
        <tr *ngFor="let p of productos">
          <td>{{ p.sku }}</td>
          <td>{{ p.nombre }}</td>
          <td>{{ p.unidad_medida_nombre || '-' }}</td>
          <td>{{ p.marca_nombre || '-' }}</td>
          <td>{{ p.activo ? 'Sí' : 'No' }}</td>
          <td>
            <button (click)="eliminar(p.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  `,
})
export class ProductosPageComponent implements OnInit {
    productos: Producto[] = [];

    constructor(private productosService: ProductosService) { }

    ngOnInit(): void {
        this.cargar();
    }

    cargar() {
        this.productosService.list().subscribe({
            next: (data) => (this.productos = data),
        });
    }

    eliminar(id: number) {
        if (!confirm('¿Eliminar producto?')) return;
        this.productosService.delete(id).subscribe({
            next: () => this.cargar(),
        });
    }
}
