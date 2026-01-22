import { NavLink, useNavigate } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import {
  Bell,
  ChevronDown,
  ClipboardList,
  LogOut,
  Moon,
  Search,
  Sun,
  User,
  ZoomIn,
  ZoomOut,
  Plus,
} from "lucide-react";

import logo from "../public/nvverde.png";

type FontScale = "sm" | "md" | "lg";

export default function Navbar() {
  const navigate = useNavigate();

  const [q, setQ] = useState("");
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const [fontScale, setFontScale] = useState<FontScale>("md");

  // ✅ Links modernos (no “botones”)
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    [
      "relative px-2.5 py-2 text-sm font-medium transition-colors",
      isActive
        ? "text-foreground"
        : "text-muted-foreground hover:text-foreground",
    ].join(" ");

  // Línea inferior activa (underline)
  const activeUnderline = ({ isActive }: { isActive: boolean }) =>
    isActive
      ? "after:absolute after:left-2.5 after:right-2.5 after:-bottom-1 after:h-[2px] after:rounded-full after:bg-foreground"
      : "";

  // Theme
  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") root.classList.add("dark");
    else root.classList.remove("dark");
  }, [theme]);

  // Font scale simple
  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove("text-sm", "text-base", "text-lg");
    if (fontScale === "sm") root.classList.add("text-sm");
    if (fontScale === "md") root.classList.add("text-base");
    if (fontScale === "lg") root.classList.add("text-lg");
  }, [fontScale]);

  const nextFontScale = useMemo(() => {
    const order: FontScale[] = ["sm", "md", "lg"];
    const idx = order.indexOf(fontScale);
    return {
      up: order[Math.min(idx + 1, order.length - 1)],
      down: order[Math.max(idx - 1, 0)],
    };
  }, [fontScale]);

  const onSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!q.trim()) return;
    navigate(`/productos?q=${encodeURIComponent(q.trim())}`);
    setQ("");
  };

  return (
    <header className="sticky top-0 z-50 border-b bg-background/85 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-6">
        {/* Fila 1 */}
        <div className="flex h-16 items-center justify-between gap-6">
          {/* IZQUIERDA: Logo + nombre (mucho mejor) */}
          <button
            onClick={() => navigate("/")}
            className="flex items-center gap-3"
            aria-label="Ir al inicio"
          >
            <div className="h-10 w-10 rounded-2xl bg-white dark:bg-slate-950 border shadow-sm grid place-items-center overflow-hidden">
              <img
                src={logo}
                alt="Logo"
                className="h-8 w-8 object-contain"
                draggable={false}
              />
            </div>

            <div className="leading-tight text-left hidden sm:block">
              <div className="text-sm font-semibold tracking-tight">
                Insumería
              </div>
              <div className="text-xs text-muted-foreground">
                Inventario y stock
              </div>
            </div>
          </button>

          {/* CENTRO: navegación limpia */}
          <nav className="hidden md:flex items-center gap-3">
            <NavLink to="/" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Inicio
            </NavLink>

            <NavLink to="/productos" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Productos
            </NavLink>

            <NavLink to="/categorias" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Categorías
            </NavLink>

            <NavLink to="/stocks" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Stock
            </NavLink>

            <NavLink to="/movimientos" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Movimientos
            </NavLink>
          </nav>

          {/* DERECHA: acciones (ordenadas) */}
          <div className="flex items-center gap-2">
            {/* Search (bonito, no “pastilla gigante”) */}
            <form
              onSubmit={onSearch}
              className="hidden lg:flex items-center gap-2 rounded-2xl border bg-card px-3 py-2 shadow-sm"
            >
              <Search className="h-4 w-4 text-muted-foreground" />
              <input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="Buscar producto…"
                className="w-64 bg-transparent text-sm outline-none placeholder:text-muted-foreground"
              />
            </form>

            {/* Botón principal */}
            <Button
              className="rounded-xl"
              onClick={() => navigate("/productos/nuevo")}
            >
              <Plus className="mr-2 h-4 w-4" />
              Nuevo
            </Button>

            <Separator orientation="vertical" className="hidden sm:block h-8 mx-1" />

            {/* Notificaciones visual */}
            <Button
              variant="outline"
              size="icon"
              className="rounded-xl relative"
              aria-label="Notificaciones"
            >
              <Bell className="h-4 w-4" />
              <span className="absolute -top-1 -right-1 h-2.5 w-2.5 rounded-full bg-red-500 ring-2 ring-background" />
            </Button>

            {/* Accesibilidad (compacto) */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="rounded-xl gap-2">
                  <span className="hidden sm:inline">Accesibilidad</span>
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>

              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>Preferencias</DropdownMenuLabel>
                <DropdownMenuSeparator />

                <DropdownMenuItem
                  onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                >
                  {theme === "dark" ? (
                    <Sun className="mr-2 h-4 w-4" />
                  ) : (
                    <Moon className="mr-2 h-4 w-4" />
                  )}
                  {theme === "dark" ? "Modo claro" : "Modo oscuro"}
                </DropdownMenuItem>

                <DropdownMenuSeparator />

                <DropdownMenuItem onClick={() => setFontScale(nextFontScale.down)}>
                  <ZoomOut className="mr-2 h-4 w-4" />
                  Disminuir texto
                </DropdownMenuItem>

                <DropdownMenuItem onClick={() => setFontScale(nextFontScale.up)}>
                  <ZoomIn className="mr-2 h-4 w-4" />
                  Aumentar texto
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Cuenta */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="rounded-xl gap-2">
                  <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-emerald-500 to-lime-400 text-white grid place-items-center text-xs font-semibold">
                    JQ
                  </div>
                  <span className="hidden md:inline text-sm">Mi cuenta</span>
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>

              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>Cuenta</DropdownMenuLabel>
                <DropdownMenuSeparator />

                <DropdownMenuItem onClick={() => navigate("/perfil")}>
                  <User className="mr-2 h-4 w-4" />
                  Ver perfil
                </DropdownMenuItem>

                <DropdownMenuItem onClick={() => navigate("/mis-movimientos")}>
                  <ClipboardList className="mr-2 h-4 w-4" />
                  Mis movimientos
                </DropdownMenuItem>

                <DropdownMenuSeparator />

                <DropdownMenuItem
                  onClick={() => navigate("/login")}
                  className="text-red-600 focus:text-red-600"
                >
                  <LogOut className="mr-2 h-4 w-4" />
                  Cerrar sesión
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>

        {/* Fila 2 (mobile): links + buscador */}
        <div className="md:hidden pb-3 space-y-3">
          <div className="flex items-center gap-2 overflow-x-auto">
            <NavLink to="/" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Inicio
            </NavLink>
            <NavLink to="/productos" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Productos
            </NavLink>
            <NavLink to="/categorias" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Categorías
            </NavLink>
            <NavLink to="/stocks" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Stock
            </NavLink>
            <NavLink to="/movimientos" className={(p) => linkClass(p) + " " + activeUnderline(p)}>
              Movimientos
            </NavLink>
          </div>

          <form
            onSubmit={onSearch}
            className="flex items-center gap-2 rounded-2xl border bg-card px-3 py-2 shadow-sm"
          >
            <Search className="h-4 w-4 text-muted-foreground" />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Buscar producto…"
              className="w-full bg-transparent text-sm outline-none placeholder:text-muted-foreground"
            />
          </form>
        </div>
      </div>
    </header>
  );
}
