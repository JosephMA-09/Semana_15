"""Punto de entrada de restaurante_app.

Crea la unica ventana principal, prepara los servicios, aplica los
estilos de la interfaz y controla el cambio entre las vistas.
"""

import tkinter as tk
from pathlib import Path

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.estilos import configurar_estilos
from ui.login_view import LoginView
from ui.main_view import MainView


class AplicacionRestaurante:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurante - Componentes y contenedores")
        self.root.geometry("940x660")
        self.root.minsize(820, 600)

        # Aplica la configuracion visual centralizada de la interfaz.
        configurar_estilos(self.root)

        # Prepara los servicios que usaran las vistas.
        ruta_base = Path(__file__).resolve().parent
        archivo_servicio = ArchivoServicio(ruta_base / "datos")
        self.restaurante_servicio = RestauranteServicio(archivo_servicio)

        self.vista_actual = None
        self.mostrar_login()

    def cambiar_vista(self, nueva_vista):
        # Reemplaza la vista actual dentro de la misma ventana.
        if self.vista_actual is not None:
            self.vista_actual.destroy()

        self.vista_actual = nueva_vista
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_login(self):
        # Muestra la primera pantalla de la aplicacion.
        vista = LoginView(
            self.root,
            self.restaurante_servicio,
            self.mostrar_interfaz_principal,
        )
        self.cambiar_vista(vista)

    def mostrar_interfaz_principal(self, usuario_actual):
        # Abre la interfaz principal despues de un acceso correcto.
        vista = MainView(
            self.root,
            self.restaurante_servicio,
            usuario_actual,
            self.mostrar_login,
        )
        self.cambiar_vista(vista)

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AplicacionRestaurante()
    app.ejecutar()
