"""Vista principal de la aplicacion.

Organiza la interfaz mediante contenedores (Frame, LabelFrame) y
componentes (Entry, Combobox, Treeview, Scrollbar, Button) distribuidos
con los gestores de geometria pack y grid.

La vista solo coordina la interaccion con el usuario: captura los datos,
llama a RestauranteServicio y muestra el resultado. Las validaciones,
las reglas de negocio y la persistencia permanecen en el servicio.

Semana 15: se agrega la seccion Ventas para evidenciar el fundamento de
manejo de eventos: accion del usuario -> boton con command= -> callback
-> RestauranteServicio -> persistencia en ventas.json -> respuesta
visual en la interfaz. Tambien se incorporan iconos desde assets/icons/.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from ui.estilos import FUENTE, PALETA, cargar_icono, cargar_imagen


class MainView(tk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg=PALETA["fondo"])
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        # Contenedor central que cambia segun la seccion seleccionada.
        self.contenido = None

        # Variables asociadas a los campos del formulario de productos.
        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.mensaje_var = tk.StringVar()

        self.tabla_productos = None
        self.categoria_combo = None
        self.estado_label = None

        # Componentes de la seccion Ventas (nueva esta semana).
        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None
        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}

        # Se conservan las referencias de las imagenes cargadas para que
        # Tkinter no las descarte de memoria.
        self.imagenes = {}

        self.construir_interfaz()

    # ==================================================================
    # Utilidades de iconos e imagenes (assets/)
    # ==================================================================
    def obtener_icono(self, nombre_base, blanco=False):
        """Carga un icono de assets/icons/ y conserva su referencia.

        Devuelve None si el archivo no existe, sin interrumpir la
        aplicacion.
        """
        clave = f"icon:{nombre_base}:{'blanco' if blanco else 'oscuro'}"

        if clave not in self.imagenes:
            self.imagenes[clave] = cargar_icono(nombre_base, blanco=blanco)

        return self.imagenes[clave]

    def crear_boton(self, contenedor, texto, comando, estilo, nombre_icono=None, blanco=False):
        """Crea un ttk.Button con command=.

        Si el icono indicado existe en assets/icons/, se agrega con
        compound="left"; si no existe, el boton se crea solo con texto
        (nunca se pasa image=None de forma explicita, para evitar
        inconsistencias entre plataformas).
        """
        icono = self.obtener_icono(nombre_icono, blanco=blanco) if nombre_icono else None

        if icono is not None:
            return ttk.Button(
                contenedor,
                text=f" {texto}",
                image=icono,
                compound="left",
                command=comando,
                style=estilo,
            )

        return ttk.Button(contenedor, text=texto, command=comando, style=estilo)

    # ==================================================================
    # Estructura general de la ventana
    # ==================================================================
    def construir_interfaz(self):
        """Arma el encabezado, la barra de navegacion, el area central
        y la barra de estado."""
        self.crear_encabezado()
        self.crear_barra_navegacion()

        # Contenedor principal: aqui se dibuja cada seccion.
        self.contenido = tk.Frame(self, bg=PALETA["fondo"], padx=20, pady=18)
        self.contenido.pack(fill="both", expand=True)

        self.crear_barra_estado()
        self.mostrar_inicio()

    def crear_encabezado(self):
        encabezado = tk.Frame(self, bg=PALETA["encabezado"], padx=24, pady=16)
        encabezado.pack(fill="x")

        # Logotipo de assets/. Se conserva la referencia en el objeto
        # para que Tkinter no descarte la imagen de memoria.
        self.imagenes["logo_encabezado"] = cargar_imagen("logo_encabezado.png")
        logo_encabezado = self.imagenes["logo_encabezado"]

        if logo_encabezado is not None:
            tk.Label(encabezado, image=logo_encabezado, bg=PALETA["encabezado"]).pack(
                side="left", padx=(0, 14)
            )

        # Contenedor con los textos, para que queden junto al logo.
        textos = tk.Frame(encabezado, bg=PALETA["encabezado"])
        textos.pack(side="left", anchor="w")

        tk.Label(
            textos,
            text="RESTAURANTE",
            bg=PALETA["encabezado"],
            fg="#FFFFFF",
            font=(FUENTE, 18, "bold"),
        ).pack(anchor="w")

        tk.Label(
            textos,
            text=f"Bienvenido, {self.usuario_actual.nombre}",
            bg=PALETA["encabezado"],
            fg=PALETA["barra"],
            font=(FUENTE, 10),
        ).pack(anchor="w", pady=(4, 0))

    def crear_barra_navegacion(self):
        barra = tk.Frame(self, bg=PALETA["barra"], padx=16, pady=8)
        barra.pack(fill="x")

        # Los iconos son oscuros porque el fondo de esta barra es claro.
        self.crear_boton(barra, "Inicio", self.mostrar_inicio, "Menu.TButton", "home").pack(
            side="left", padx=(0, 8)
        )
        self.crear_boton(
            barra, "Productos", self.mostrar_productos, "Menu.TButton", "productos"
        ).pack(side="left", padx=(0, 8))
        self.crear_boton(
            barra, "Usuarios", self.mostrar_usuarios, "Menu.TButton", "usuarios"
        ).pack(side="left", padx=(0, 8))
        self.crear_boton(
            barra, "Ventas", self.mostrar_ventas, "Menu.TButton", "ventas"
        ).pack(side="left", padx=(0, 8))
        self.crear_boton(
            barra,
            "Cerrar sesion",
            self.cerrar_sesion,
            "Peligro.TButton",
            "logout",
            blanco=True,
        ).pack(side="right")

    def crear_barra_estado(self):
        barra_estado = tk.Frame(self, bg=PALETA["barra"], padx=16, pady=6)
        barra_estado.pack(fill="x", side="bottom")

        self.estado_label = tk.Label(
            barra_estado,
            text="",
            bg=PALETA["barra"],
            fg=PALETA["texto"],
            font=(FUENTE, 9),
        )
        self.estado_label.pack(side="left")
        self.actualizar_barra_estado()

    def actualizar_barra_estado(self):
        """Refresca los totales mostrados al pie de la ventana."""
        if self.estado_label is None:
            return

        self.estado_label.config(
            text=(
                f"Productos: {self.restaurante_servicio.cantidad_productos()}  |  "
                f"Usuarios: {self.restaurante_servicio.cantidad_usuarios()}  |  "
                f"Ventas: {self.restaurante_servicio.cantidad_ventas()}  |  "
                "Persistencia: archivos JSON"
            )
        )

    def limpiar_contenido(self):
        """Vacia el contenedor central antes de dibujar otra seccion."""
        for widget in self.contenido.winfo_children():
            widget.destroy()

        # Al cambiar de seccion, las referencias a componentes de la
        # seccion anterior dejan de ser validas.
        self.tabla_productos = None
        self.categoria_combo = None
        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None

    # ==================================================================
    # Seccion: Inicio
    # ==================================================================
    def mostrar_inicio(self):
        self.limpiar_contenido()

        tarjeta = tk.Frame(self.contenido, bg=PALETA["tarjeta"], padx=24, pady=22)
        tarjeta.pack(fill="both", expand=True)

        tk.Label(
            tarjeta,
            text="Panel principal",
            bg=PALETA["tarjeta"],
            fg=PALETA["encabezado"],
            font=(FUENTE, 16, "bold"),
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text="Seleccione una opcion de la barra superior para gestionar la informacion.",
            bg=PALETA["tarjeta"],
            fg=PALETA["suave"],
            font=(FUENTE, 10),
        ).pack(anchor="w", pady=(6, 18))

        resumen = tk.Frame(tarjeta, bg=PALETA["tarjeta"])
        resumen.pack(fill="x")

        self.crear_tarjeta_resumen(
            resumen,
            0,
            "Productos registrados",
            str(self.restaurante_servicio.cantidad_productos()),
        )
        self.crear_tarjeta_resumen(
            resumen,
            1,
            "Usuarios registrados",
            str(self.restaurante_servicio.cantidad_usuarios()),
        )
        self.crear_tarjeta_resumen(
            resumen,
            2,
            "Ventas registradas",
            str(self.restaurante_servicio.cantidad_ventas()),
        )

    def crear_tarjeta_resumen(self, contenedor, columna, titulo, valor):
        """Muestra un dato resumido usando grid dentro del contenedor."""
        contenedor.columnconfigure(columna, weight=1)

        caja = tk.Frame(contenedor, bg=PALETA["barra"], padx=18, pady=14)
        caja.grid(row=0, column=columna, sticky="ew", padx=(0, 12))

        tk.Label(
            caja,
            text=valor,
            bg=PALETA["barra"],
            fg=PALETA["encabezado"],
            font=(FUENTE, 20, "bold"),
        ).pack(anchor="w")

        tk.Label(
            caja,
            text=titulo,
            bg=PALETA["barra"],
            fg=PALETA["texto"],
            font=(FUENTE, 9),
        ).pack(anchor="w")

    # ==================================================================
    # Seccion: Productos (formulario + acciones + visualizacion)
    # ==================================================================
    def mostrar_productos(self):
        self.limpiar_contenido()
        self.mensaje_var.set("")

        # El contenedor de productos se organiza con grid en dos filas:
        # fila 0 -> formulario y acciones, fila 1 -> tabla de productos.
        contenedor = tk.Frame(self.contenido, bg=PALETA["fondo"])
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(1, weight=1)

        self.crear_formulario_producto(contenedor)
        self.crear_tabla_productos(contenedor)

        self.limpiar_formulario()
        self.refrescar_tabla_productos()

    def crear_formulario_producto(self, contenedor):
        """Formulario de captura dentro de un LabelFrame (contenedor)."""
        formulario = ttk.LabelFrame(
            contenedor,
            text=" Datos del producto ",
            style="Seccion.TLabelframe",
            padding=16,
        )
        formulario.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        # Dos parejas de columnas (etiqueta + campo) que se expanden.
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        self.crear_campo(formulario, "Codigo", self.codigo_var, 0, 0)
        self.crear_campo(formulario, "Nombre", self.nombre_var, 0, 2)

        # Combobox: permite elegir una categoria existente o escribir una nueva.
        ttk.Label(formulario, text="Categoria", style="Tarjeta.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=(10, 0)
        )
        self.categoria_combo = ttk.Combobox(
            formulario,
            textvariable=self.categoria_var,
            values=self.restaurante_servicio.obtener_categorias(),
            width=22,
        )
        self.categoria_combo.grid(row=1, column=1, sticky="ew", padx=(0, 18), pady=(10, 0))

        self.crear_campo(formulario, "Precio", self.precio_var, 1, 2, pady=(10, 0))
        self.crear_campo(formulario, "Stock", self.stock_var, 2, 0, pady=(10, 0))

        # Contenedor de acciones: agrupa los botones de operacion.
        acciones = ttk.Frame(formulario, style="Tarjeta.TFrame")
        acciones.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(18, 0))

        self.crear_boton(
            acciones, "Registrar", self.registrar_producto, "Accion.TButton", "add", blanco=True
        ).pack(side="left", padx=(0, 8))

        self.crear_boton(
            acciones, "Cargar", self.cargar_producto, "Accion.TButton", "search", blanco=True
        ).pack(side="left", padx=(0, 8))

        self.crear_boton(
            acciones, "Actualizar", self.actualizar_producto, "Accion.TButton", "edit", blanco=True
        ).pack(side="left", padx=(0, 8))

        self.crear_boton(
            acciones, "Eliminar", self.eliminar_producto, "Peligro.TButton", "delete", blanco=True
        ).pack(side="left", padx=(0, 8))

        self.crear_boton(
            acciones, "Limpiar", self.limpiar_formulario, "Menu.TButton", "clean"
        ).pack(side="left")

        # Mensaje de retroalimentacion sobre la ultima operacion.
        tk.Label(
            formulario,
            textvariable=self.mensaje_var,
            bg=PALETA["tarjeta"],
            fg=PALETA["suave"],
            font=(FUENTE, 9),
            anchor="w",
        ).grid(row=4, column=0, columnspan=4, sticky="ew", pady=(12, 0))

    def crear_campo(self, contenedor, etiqueta, variable, fila, columna, pady=(0, 0)):
        """Crea una etiqueta y su campo de entrada ubicados con grid."""
        ttk.Label(contenedor, text=etiqueta, style="Tarjeta.TLabel").grid(
            row=fila, column=columna, sticky="w", padx=(0, 8), pady=pady
        )
        entrada = ttk.Entry(contenedor, textvariable=variable, width=24)
        entrada.grid(row=fila, column=columna + 1, sticky="ew", padx=(0, 18), pady=pady)
        return entrada

    def crear_tabla_productos(self, contenedor):
        """Tabla de productos (Treeview) con barra de desplazamiento."""
        seccion = ttk.LabelFrame(
            contenedor,
            text=" Productos registrados ",
            style="Seccion.TLabelframe",
            padding=12,
        )
        seccion.grid(row=1, column=0, sticky="nsew")
        seccion.columnconfigure(0, weight=1)
        seccion.rowconfigure(0, weight=1)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(
            seccion,
            columns=columnas,
            show="headings",
            height=8,
            style="Tabla.Treeview",
        )

        encabezados = {
            "codigo": ("Codigo", 90),
            "nombre": ("Nombre", 220),
            "categoria": ("Categoria", 150),
            "precio": ("Precio", 90),
            "stock": ("Stock", 80),
        }

        for columna, (titulo, ancho) in encabezados.items():
            self.tabla_productos.heading(columna, text=titulo)
            anclaje = "w" if columna in ("nombre", "categoria") else "center"
            self.tabla_productos.column(columna, width=ancho, anchor=anclaje)

        self.tabla_productos.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(
            seccion, orient="vertical", command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")

        ttk.Label(
            seccion,
            text="Escriba el codigo y use Cargar para traer un producto al formulario.",
            style="Tarjeta.TLabel",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def refrescar_tabla_productos(self):
        """Vuelve a pedir los productos al servicio y redibuja la tabla."""
        if self.tabla_productos is None:
            return

        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"{producto.precio:.2f}",
                    producto.stock,
                ),
            )

        # Mantiene el Combobox alineado con las categorias vigentes.
        if self.categoria_combo is not None:
            self.categoria_combo.configure(
                values=self.restaurante_servicio.obtener_categorias()
            )

        self.actualizar_barra_estado()

    # ==================================================================
    # Operaciones de productos (delegadas al servicio)
    # ==================================================================
    def registrar_producto(self):
        try:
            producto = self.restaurante_servicio.registrar_producto(
                self.codigo_var.get(),
                self.nombre_var.get(),
                self.categoria_var.get(),
                self.precio_var.get(),
                self.stock_var.get(),
            )
        except ValueError as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return

        self.refrescar_tabla_productos()
        self.limpiar_formulario()
        self.informar(f"Producto {producto.codigo} registrado correctamente.")

    def cargar_producto(self):
        codigo = self.codigo_var.get().strip()

        if not codigo:
            messagebox.showwarning("Dato requerido", "Ingrese el codigo del producto.")
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)

        if producto is None:
            messagebox.showinfo("Sin resultados", "No existe un producto con ese codigo.")
            return

        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(f"{producto.precio:.2f}")
        self.stock_var.set(str(producto.stock))
        self.informar(f"Producto {producto.codigo} cargado en el formulario.")

    def actualizar_producto(self):
        try:
            producto = self.restaurante_servicio.actualizar_producto(
                self.codigo_var.get(),
                self.nombre_var.get(),
                self.categoria_var.get(),
                self.precio_var.get(),
                self.stock_var.get(),
            )
        except ValueError as error:
            messagebox.showerror("No se pudo actualizar", str(error))
            return

        self.refrescar_tabla_productos()
        self.informar(f"Producto {producto.codigo} actualizado correctamente.")

    def eliminar_producto(self):
        codigo = self.codigo_var.get().strip()

        if not codigo:
            messagebox.showwarning("Dato requerido", "Ingrese el codigo del producto.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            f"Desea eliminar el producto {codigo}?",
        )

        if not confirmar:
            return

        try:
            self.restaurante_servicio.eliminar_producto(codigo)
        except ValueError as error:
            messagebox.showerror("No se pudo eliminar", str(error))
            return

        self.refrescar_tabla_productos()
        self.limpiar_formulario()
        self.informar(f"Producto {codigo} eliminado correctamente.")

    def limpiar_formulario(self):
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.stock_var.set("")

    def informar(self, mensaje):
        """Muestra el resultado de la ultima operacion en el formulario."""
        self.mensaje_var.set(mensaje)

    # ==================================================================
    # Seccion: Usuarios
    # ==================================================================
    def mostrar_usuarios(self):
        self.limpiar_contenido()

        seccion = ttk.LabelFrame(
            self.contenido,
            text=" Usuarios registrados ",
            style="Seccion.TLabelframe",
            padding=12,
        )
        seccion.pack(fill="both", expand=True)
        seccion.columnconfigure(0, weight=1)
        seccion.rowconfigure(0, weight=1)

        columnas = ("identificacion", "nombre", "usuario")
        tabla = ttk.Treeview(
            seccion,
            columns=columnas,
            show="headings",
            height=10,
            style="Tabla.Treeview",
        )

        encabezados = {
            "identificacion": ("Identificacion", 140),
            "nombre": ("Nombre", 260),
            "usuario": ("Usuario de acceso", 180),
        }

        for columna, (titulo, ancho) in encabezados.items():
            tabla.heading(columna, text=titulo)
            anclaje = "w" if columna == "nombre" else "center"
            tabla.column(columna, width=ancho, anchor=anclaje)

        for usuario in self.restaurante_servicio.listar_usuarios():
            tabla.insert(
                "",
                tk.END,
                values=(usuario.identificacion, usuario.nombre, usuario.usuario),
            )

        tabla.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(seccion, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")

        ttk.Label(
            seccion,
            text="La informacion de usuarios se consulta a traves de RestauranteServicio.",
            style="Tarjeta.TLabel",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))

    # ==================================================================
    # Seccion: Ventas (nueva esta semana)
    # ==================================================================
    def mostrar_ventas(self):
        self.limpiar_contenido()

        # El contenedor de ventas se organiza con grid en dos columnas:
        # columna 0 -> formulario de registro, columna 1 -> tabla.
        contenedor = tk.Frame(self.contenido, bg=PALETA["fondo"])
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        self.crear_formulario_venta(contenedor)
        self.crear_tabla_ventas(contenedor)

        self.refrescar_tabla_ventas()

    def crear_formulario_venta(self, contenedor):
        """Formulario para relacionar un usuario existente con un
        producto existente y disparar el registro de la venta."""
        formulario = ttk.LabelFrame(
            contenedor,
            text=" Registrar venta ",
            style="Seccion.TLabelframe",
            padding=16,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 16))

        ttk.Label(formulario, text="Usuario", style="Tarjeta.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )
        self.usuario_venta_combo = ttk.Combobox(
            formulario,
            values=list(self.obtener_opciones_usuarios_venta().keys()),
            state="readonly",
            width=30,
        )
        self.usuario_venta_combo.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        ttk.Label(formulario, text="Producto", style="Tarjeta.TLabel").grid(
            row=2, column=0, sticky="w", pady=(0, 6)
        )
        self.producto_venta_combo = ttk.Combobox(
            formulario,
            values=list(self.obtener_opciones_productos_venta().keys()),
            state="readonly",
            width=30,
        )
        self.producto_venta_combo.grid(row=3, column=0, sticky="ew", pady=(0, 18))

        # El boton usa command= para ejecutar el callback registrar_venta
        # al hacer clic: esta es la accion que dispara todo el flujo.
        self.crear_boton(
            formulario,
            "Registrar venta",
            self.registrar_venta,
            "Accion.TButton",
            "add",
            blanco=True,
        ).grid(row=4, column=0, sticky="ew")

        ttk.Label(
            formulario,
            text="Seleccione un usuario y un producto ya registrados.",
            style="Tarjeta.TLabel",
            wraplength=220,
        ).grid(row=5, column=0, sticky="w", pady=(12, 0))

    def obtener_opciones_usuarios_venta(self):
        """Arma el texto visible del Combobox y lo asocia a la
        identificacion real que se envia al servicio."""
        self.opciones_usuarios_venta = {
            f"{usuario.identificacion} - {usuario.nombre}": usuario.identificacion
            for usuario in self.restaurante_servicio.listar_usuarios()
        }
        return self.opciones_usuarios_venta

    def obtener_opciones_productos_venta(self):
        """Arma el texto visible del Combobox y lo asocia al codigo
        real del producto que se envia al servicio."""
        self.opciones_productos_venta = {
            f"{producto.codigo} - {producto.nombre}": producto.codigo
            for producto in self.restaurante_servicio.listar_productos()
        }
        return self.opciones_productos_venta

    def crear_tabla_ventas(self, contenedor):
        """Tabla de ventas (Treeview) con barra de desplazamiento."""
        seccion = ttk.LabelFrame(
            contenedor,
            text=" Ventas registradas ",
            style="Seccion.TLabelframe",
            padding=12,
        )
        seccion.grid(row=0, column=1, sticky="nsew")
        seccion.columnconfigure(0, weight=1)
        seccion.rowconfigure(0, weight=1)

        columnas = ("identificador", "usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(
            seccion,
            columns=columnas,
            show="headings",
            height=10,
            style="Tabla.Treeview",
        )

        encabezados = {
            "identificador": ("Venta", 80),
            "usuario": ("Usuario", 220),
            "producto": ("Producto", 220),
            "fecha": ("Fecha", 110),
        }

        for columna, (titulo, ancho) in encabezados.items():
            self.tabla_ventas.heading(columna, text=titulo)
            anclaje = "w" if columna in ("usuario", "producto") else "center"
            self.tabla_ventas.column(columna, width=ancho, anchor=anclaje)

        self.tabla_ventas.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(seccion, orient="vertical", command=self.tabla_ventas.yview)
        self.tabla_ventas.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")

    def registrar_venta(self):
        """Callback ejecutado por el boton 'Registrar venta' (command=).

        Obtiene la seleccion de los Combobox, delega el registro a
        RestauranteServicio y actualiza la interfaz con el resultado.
        No contiene reglas del restaurante: solo coordina la accion.
        """
        if self.usuario_venta_combo is None or self.producto_venta_combo is None:
            return

        usuario_id = self.opciones_usuarios_venta.get(self.usuario_venta_combo.get(), "")
        producto_codigo = self.opciones_productos_venta.get(
            self.producto_venta_combo.get(), ""
        )

        try:
            # RestauranteServicio valida la seleccion, registra la venta
            # y la persiste en ventas.json.
            self.restaurante_servicio.registrar_venta(usuario_id, producto_codigo)
        except ValueError as error:
            messagebox.showerror("No se pudo registrar la venta", str(error))
            return

        self.usuario_venta_combo.set("")
        self.producto_venta_combo.set("")
        self.refrescar_tabla_ventas()
        messagebox.showinfo("Ventas", "Venta registrada correctamente.")

    def refrescar_tabla_ventas(self):
        """Vuelve a pedir las ventas al servicio y redibuja la tabla,
        para que el usuario observe de inmediato el resultado."""
        if self.tabla_ventas is None:
            return

        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)

        for venta in self.restaurante_servicio.listar_ventas():
            usuario = self.restaurante_servicio.buscar_usuario(venta.usuario_id)
            producto = self.restaurante_servicio.buscar_producto(venta.producto_codigo)

            texto_usuario = (
                venta.usuario_id if usuario is None else f"{usuario.identificacion} - {usuario.nombre}"
            )
            texto_producto = (
                venta.producto_codigo if producto is None else f"{producto.codigo} - {producto.nombre}"
            )

            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(venta.identificador, texto_usuario, texto_producto, venta.fecha),
            )

        self.actualizar_barra_estado()

    # ==================================================================
    # Otras acciones
    # ==================================================================
    def cerrar_sesion(self):
        # Regresa al login sin crear otra ventana ni otro mainloop.
        self.al_cerrar_sesion()
