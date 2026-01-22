import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Producto } from '../models/producto.model';

@Injectable({ providedIn: 'root' })
export class ProductosService {
  private url = 'http://127.0.0.1:8000/api/productos/';

  constructor(private http: HttpClient) { }

  list(): Observable<Producto[]> {
    return this.http.get<Producto[]>(this.url);
  }

  create(data: Partial<Producto>): Observable<Producto> {
    return this.http.post<Producto>(this.url, data);
  }

  update(id: number, data: Partial<Producto>): Observable<Producto> {
    return this.http.put<Producto>(`${this.url}${id}/`, data);
  }

  delete(id: number): Observable<any> {
    return this.http.delete(`${this.url}${id}/`);
  }
}
