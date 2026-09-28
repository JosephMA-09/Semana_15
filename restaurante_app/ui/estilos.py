"""Configuracion visual centralizada de la interfaz.

Reune la paleta de colores, las fuentes, los estilos ttk reutilizables y
la carga de los recursos graficos de la carpeta assets/, para que las
vistas no repitan configuraciones y la aplicacion mantenga una
apariencia coherente.
"""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

# Carpeta con los recursos visuales del proyecto (ui/ -> restaurante_app/assets).
CARPETA_ASSETS = Path(__file__).resolve().parent.parent / "assets"


def cargar_imagen(nombre_archivo):
    """Carga una imagen de la carpeta assets/.

    Devuelve None si el archivo no existe o si el formato no puede
    mostrarse en el equipo, de modo que la interfaz siga funcionando
    aunque el recurso grafico no este disponible.
    """
    ruta = CARPETA_ASSETS / nombre_archivo

    if not ruta.exists():
        return None

    try:
        return tk.PhotoImage(file=str(ruta))
    except tk.TclError:
        return None


def cargar_icono(nombre_base, blanco=False):
    """Carga un icono de assets/icons/.

    Cada icono tiene una variante oscura (para botones con fondo claro)
    y una variante blanca (para botones con fondo de color). Si el
    archivo no existe, devuelve None y el boton se muestra solo con
    texto, sin interrumpir la aplicacion.
    """
    sufijo = "_blanco" if blanco else ""
    return cargar_imagen(f"icons/{nombre_base}{sufijo}.png")

PALETA = {
    "fondo": "#F4F6F9",
    "tarjeta": "#FFFFFF",
    "encabezado": "#1F2A44",
    "barra": "#DBEAFE",
    "texto": "#243447",
    "suave": "#667085",
    "acento": "#2563EB",
    "acento_oscuro": "#1D4ED8",
    "peligro": "#E11D48",
    "peligro_oscuro": "#BE123C",
    "exito": "#0F9D58",
    "borde": "#D8DEE7",
}

FUENTE = "Segoe UI"


def configurar_estilos(root):
    """Aplica el tema ttk y define los estilos usados por las vistas."""
    root.configure(bg=PALETA["fondo"])

    estilo = ttk.Style(root)

    try:
        estilo.theme_use("clam")
    except Exception:
        # Si el tema no esta disponible se conserva el tema por defecto.
        pass

    estilo.configure(".", font=(FUENTE, 10), background=PALETA["fondo"])

    # Contenedores
    estilo.configure("TFrame", background=PALETA["fondo"])
    estilo.configure("Tarjeta.TFrame", background=PALETA["tarjeta"])
    estilo.configure(
        "Seccion.TLabelframe",
        background=PALETA["tarjeta"],
        borderwidth=1,
        relief="solid",
    )
    estilo.configure(
        "Seccion.TLabelframe.Label",
        background=PALETA["tarjeta"],
        foreground=PALETA["encabezado"],
        font=(FUENTE, 10, "bold"),
    )

    # Etiquetas
    estilo.configure("TLabel", background=PALETA["fondo"], foreground=PALETA["texto"])
    estilo.configure("Tarjeta.TLabel", background=PALETA["tarjeta"], foreground=PALETA["texto"])
    estilo.configure(
        "Titulo.TLabel",
        background=PALETA["fondo"],
        foreground=PALETA["encabezado"],
        font=(FUENTE, 16, "bold"),
    )
    estilo.configure(
        "Suave.TLabel",
        background=PALETA["fondo"],
        foreground=PALETA["suave"],
    )

    # Botones
    estilo.configure(
        "Accion.TButton",
        background=PALETA["acento"],
        foreground="#FFFFFF",
        font=(FUENTE, 10, "bold"),
        padding=(12, 7),
        borderwidth=0,
    )
    estilo.map("Accion.TButton", background=[("active", PALETA["acento_oscuro"])])

    estilo.configure(
        "Peligro.TButton",
        background=PALETA["peligro"],
        foreground="#FFFFFF",
        font=(FUENTE, 10, "bold"),
        padding=(12, 7),
        borderwidth=0,
    )
    estilo.map("Peligro.TButton", background=[("active", PALETA["peligro_oscuro"])])

    estilo.configure(
        "Menu.TButton",
        background=PALETA["barra"],
        foreground=PALETA["encabezado"],
        font=(FUENTE, 10, "bold"),
        padding=(12, 8),
        borderwidth=0,
    )
    estilo.map("Menu.TButton", background=[("active", "#C7DDFF")])

    # Tabla
    estilo.configure(
        "Tabla.Treeview",
        background=PALETA["tarjeta"],
        fieldbackground=PALETA["tarjeta"],
        foreground=PALETA["texto"],
        rowheight=26,
        borderwidth=0,
    )
    estilo.configure(
        "Tabla.Treeview.Heading",
        background=PALETA["barra"],
        foreground=PALETA["encabezado"],
        font=(FUENTE, 10, "bold"),
    )
    estilo.map("Tabla.Treeview", background=[("selected", PALETA["acento"])])
