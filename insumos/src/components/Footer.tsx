import { Instagram, Facebook, MessageCircle } from "lucide-react";

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="mt-12 border-t bg-gradient-to-b from-muted/40 to-background">
      <div className="mx-auto max-w-6xl px-4 py-10">
        <div className="grid gap-10 md:grid-cols-3">
          {/* Marca */}
          <div className="space-y-3">
            <h3 className="text-lg font-semibold tracking-tight">Insumería</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Sistema de inventario para controlar productos, stock y movimientos
              de manera simple y rápida.
            </p>

            {/* Redes coloridas */}
            <div className="flex items-center gap-3 pt-1">
              <a
                href="#"
                aria-label="Instagram"
                className="h-11 w-11 rounded-2xl grid place-items-center shadow-sm transition hover:scale-[1.05]
                           bg-gradient-to-br from-pink-500 to-orange-400 text-white"
              >
                <Instagram className="h-5 w-5" />
              </a>

              <a
                href="#"
                aria-label="Facebook"
                className="h-11 w-11 rounded-2xl grid place-items-center shadow-sm transition hover:scale-[1.05]
                           bg-gradient-to-br from-blue-600 to-sky-400 text-white"
              >
                <Facebook className="h-5 w-5" />
              </a>

              <a
                href="#"
                aria-label="WhatsApp"
                className="h-11 w-11 rounded-2xl grid place-items-center shadow-sm transition hover:scale-[1.05]
                           bg-gradient-to-br from-emerald-500 to-lime-400 text-white"
              >
                <MessageCircle className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Info */}
          <div className="space-y-3">
            <h4 className="text-sm font-semibold">Información</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a
                  href="/quienes-somos"
                  className="text-muted-foreground hover:text-foreground transition-colors"
                >
                  Quiénes somos
                </a>
              </li>
              <li>
                <a
                  href="/terminos"
                  className="text-muted-foreground hover:text-foreground transition-colors"
                >
                  Términos y condiciones
                </a>
              </li>
              <li>
                <a
                  href="/privacidad"
                  className="text-muted-foreground hover:text-foreground transition-colors"
                >
                  Privacidad
                </a>
              </li>
            </ul>
          </div>

          {/* Contacto */}
          <div className="space-y-3">
            <h4 className="text-sm font-semibold">Contacto</h4>
            <div className="space-y-2 text-sm text-muted-foreground">
              <p>
                Correo:{" "}
                <a
                  href="mailto:contacto@insumeria.cl"
                  className="text-foreground/90 hover:text-foreground transition-colors underline underline-offset-4 decoration-muted-foreground/40 hover:decoration-foreground"
                >
                  contacto@insumeria.cl
                </a>
              </p>
              <p>Teléfono: +56 9 0000 0000</p>
            </div>
          </div>
        </div>

        {/* Línea final */}
        <div className="mt-10 flex flex-col gap-2 border-t pt-4 text-xs text-muted-foreground sm:flex-row sm:items-center sm:justify-between">
          <p>© {year} Insumería. Todos los derechos reservados.</p>
          <p className="hidden sm:block">Gestión profesional de inventario</p>
        </div>
      </div>
    </footer>
  );
}
