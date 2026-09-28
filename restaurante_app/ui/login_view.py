"""Vista de acceso simulado.

Usa contenedores (Frame, LabelFrame) y componentes (Label, Entry,
Button) organizados con grid. La validacion de credenciales se delega
a RestauranteServicio.
"""

import tkinter as tk
from tkinter import ttk

from ui.estilos import FUENTE, PALETA, cargar_imagen


class LoginView(tk.Frame):
    def __init__(self, master, restaurante_servicio, al_iniciar_sesion):
        super().__init__(master, bg=PALETA["fondo"])
        self.restaurante_servicio = restaurante_servicio
        self.al_iniciar_sesion = al_iniciar_sesion

        self.usuario_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.mensaje_var = tk.StringVar()

        self.construir_interfaz()

    def construir_interfaz(self):
        # Tarjeta centrada que agrupa todo el formulario de acceso.
        tarjeta = tk.Frame(self, bg=PALETA["tarjeta"], padx=32, pady=28)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        # Recurso grafico de assets/. Se conserva la referencia en el
        # objeto para que Tkinter no descarte la imagen de memoria.
        self.logo = cargar_imagen("logo_restaurante.png")

        if self.logo is not None:
            tk.Label(tarjeta, image=self.logo, bg=PALETA["tarjeta"]).pack(pady=(0, 10))

        tk.Label(
            tarjeta,
            text="Restaurante",
            bg=PALETA["tarjeta"],
            fg=PALETA["encabezado"],
            font=(FUENTE, 22, "bold"),
        ).pack(pady=(0, 4))

        tk.Label(
            tarjeta,
            text="Inicio de sesion",
            bg=PALETA["tarjeta"],
            fg=PALETA["suave"],
            font=(FUENTE, 10),
        ).pack(pady=(0, 20))

        # LabelFrame: contenedor con titulo para las credenciales.
        credenciales = ttk.LabelFrame(
            tarjeta,
            text=" Credenciales ",
            style="Seccion.TLabelframe",
            padding=16,
        )
        credenciales.pack(fill="x")
        credenciales.columnconfigure(1, weight=1)

        ttk.Label(credenciales, text="Usuario", style="Tarjeta.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 8)
        )
        usuario_entry = ttk.Entry(credenciales, textvariable=self.usuario_var, width=26)
        usuario_entry.grid(row=0, column=1, sticky="ew", pady=(0, 8))
        usuario_entry.focus()

        ttk.Label(credenciales, text="Contrasena", style="Tarjeta.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 10)
        )
        contrasena_entry = ttk.Entry(
            credenciales,
            textvariable=self.contrasena_var,
            width=26,
            show="*",
        )
        contrasena_entry.grid(row=1, column=1, sticky="ew")
        contrasena_entry.bind("<Return>", lambda evento: self.iniciar_sesion())

        tk.Label(
            tarjeta,
            textvariable=self.mensaje_var,
            bg=PALETA["tarjeta"],
            fg=PALETA["peligro"],
            font=(FUENTE, 9),
        ).pack(pady=(12, 10))

        ttk.Button(
            tarjeta,
            text="Iniciar sesion",
            command=self.iniciar_sesion,
            style="Accion.TButton",
        ).pack(fill="x")

    def iniciar_sesion(self):
        # Obtiene los valores escritos y solicita la validacion al servicio.
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get().strip()

        if not usuario or not contrasena:
            self.mensaje_var.set("Ingrese usuario y contrasena.")
            return

        usuario_validado = self.restaurante_servicio.validar_acceso(usuario, contrasena)

        if usuario_validado is None:
            self.mensaje_var.set("Credenciales incorrectas.")
            return

        self.mensaje_var.set("")
        self.al_iniciar_sesion(usuario_validado)
