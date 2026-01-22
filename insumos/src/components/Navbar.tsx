import { NavLink } from "react-router-dom";

export default function Navbar() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-md text-sm font-medium ${
      isActive ? "bg-gray-900 text-white" : "text-gray-800 hover:bg-gray-200"
    }`;

  return (
    <header className="border-b bg-white">
      <nav className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
        <div className="font-semibold text-lg">Bodega</div>

        <div className="flex gap-2">
          <NavLink to="/" className={linkClass}>
            Inicio
          </NavLink>

          <NavLink to="/productos" className={linkClass}>
            Productos
          </NavLink>

          <NavLink to="/categorias" className={linkClass}>
            Categorías
          </NavLink>
        </div>
      </nav>
    </header>
  );
}
