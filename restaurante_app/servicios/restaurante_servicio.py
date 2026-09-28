from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    """Concentra las reglas de negocio y el acceso a los datos.

    Las vistas (LoginView, MainView) NUNCA leen ni escriben JSON
    directamente: solicitan cada operacion a este servicio, que valida,
    actualiza la coleccion en memoria y persiste el resultado mediante
    ArchivoServicio.
    """

    ARCHIVO_PRODUCTOS = "productos.json"
    ARCHIVO_USUARIOS = "usuarios.json"
    ARCHIVO_VENTAS = "ventas.json"

    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    # ------------------------------------------------------------------
    # Carga y persistencia
    # ------------------------------------------------------------------
    def cargar_datos(self):
        # Carga los datos persistidos y los convierte en objetos.
        usuarios_json = self.archivo_servicio.leer_json(self.ARCHIVO_USUARIOS)
        productos_json = self.archivo_servicio.leer_json(self.ARCHIVO_PRODUCTOS)
        ventas_json = self.archivo_servicio.leer_json(self.ARCHIVO_VENTAS)

        self.usuarios = [
            Usuario(
                datos.get("identificacion", ""),
                datos.get("nombre", ""),
                datos.get("usuario", ""),
                datos.get("contraseña", datos.get("contrasena", "")),
            )
            for datos in usuarios_json
        ]

        self.productos = [
            Producto(
                datos.get("codigo", ""),
                datos.get("nombre", ""),
                datos.get("categoria", ""),
                datos.get("precio", 0),
                datos.get("stock", 0),
            )
            for datos in productos_json
        ]

        # Semana 15: carga las ventas persistidas para mostrarlas en la interfaz.
        self.ventas = [
            Venta(
                datos.get("identificador", ""),
                datos.get("usuario_id", ""),
                datos.get("producto_codigo", ""),
                datos.get("fecha", ""),
            )
            for datos in ventas_json
        ]

    def guardar_productos(self):
        # Convierte los objetos Producto a diccionarios y los persiste.
        datos = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "precio": producto.precio,
                "stock": producto.stock,
            }
            for producto in self.productos
        ]
        self.archivo_servicio.escribir_json(self.ARCHIVO_PRODUCTOS, datos)

    def guardar_ventas(self):
        # Convierte los objetos Venta a diccionarios y los persiste.
        datos = [
            {
                "identificador": venta.identificador,
                "usuario_id": venta.usuario_id,
                "producto_codigo": venta.producto_codigo,
                "fecha": venta.fecha,
            }
            for venta in self.ventas
        ]
        self.archivo_servicio.escribir_json(self.ARCHIVO_VENTAS, datos)

    # ------------------------------------------------------------------
    # Acceso
    # ------------------------------------------------------------------
    def validar_acceso(self, usuario, contrasena):
        # Verifica si las credenciales coinciden con un usuario cargado.
        for usuario_registrado in self.usuarios:
            if (
                usuario_registrado.usuario == usuario
                and usuario_registrado.contrasena == contrasena
            ):
                return usuario_registrado

        return None

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_productos(self):
        return len(self.productos)

    def cantidad_ventas(self):
        return len(self.ventas)

    def listar_usuarios(self):
        # Entrega los usuarios cargados para mostrarlos en la interfaz.
        return self.usuarios

    def listar_productos(self):
        # Entrega los productos cargados para mostrarlos en la interfaz.
        return self.productos

    def listar_ventas(self):
        # Entrega las ventas cargadas para mostrarlas en la interfaz.
        return self.ventas

    def buscar_producto(self, codigo):
        # Busca un producto por su codigo; devuelve None si no existe.
        codigo = str(codigo).strip()

        for producto in self.productos:
            if producto.codigo == codigo:
                return producto

        return None

    def buscar_usuario(self, identificacion):
        # Busca un usuario por su identificacion; devuelve None si no existe.
        identificacion = str(identificacion).strip()

        for usuario in self.usuarios:
            if usuario.identificacion == identificacion:
                return usuario

        return None

    def obtener_categorias(self):
        # Entrega las categorias disponibles para alimentar el Combobox.
        categorias = {producto.categoria for producto in self.productos if producto.categoria}
        return sorted(categorias)

    # ------------------------------------------------------------------
    # Operaciones sobre productos
    # ------------------------------------------------------------------
    def registrar_producto(self, codigo, nombre, categoria, precio, stock):
        # Valida que el codigo no se repita y crea el nuevo producto.
        if self.buscar_producto(codigo) is not None:
            raise ValueError("Ya existe un producto registrado con ese codigo.")

        producto = Producto(codigo, nombre, categoria, precio, stock)
        self.productos.append(producto)
        self.guardar_productos()
        return producto

    def actualizar_producto(self, codigo, nombre, categoria, precio, stock):
        # Actualiza los datos de un producto existente.
        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ValueError("No existe un producto con ese codigo.")

        # Cada asignacion pasa por el @property del modelo, que valida.
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock

        self.guardar_productos()
        return producto

    def eliminar_producto(self, codigo):
        # Elimina un producto existente de la coleccion.
        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ValueError("No existe un producto con ese codigo.")

        self.productos.remove(producto)
        self.guardar_productos()
        return producto

    # ------------------------------------------------------------------
    # Operaciones sobre ventas
    # ------------------------------------------------------------------
    def generar_identificador_venta(self):
        # Genera un identificador secuencial simple para la nueva venta.
        siguiente = len(self.ventas) + 1
        return f"V{siguiente:03d}"

    def registrar_venta(self, usuario_id, producto_codigo):
        # Relaciona un usuario existente con un producto existente y
        # registra la operacion con la fecha del dia.
        usuario_id = str(usuario_id).strip()
        producto_codigo = str(producto_codigo).strip()

        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not producto_codigo:
            raise ValueError("Debe seleccionar un producto.")
        if self.buscar_usuario(usuario_id) is None:
            raise ValueError("El usuario seleccionado no existe.")
        if self.buscar_producto(producto_codigo) is None:
            raise ValueError("El producto seleccionado no existe.")

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_id,
            producto_codigo,
            date.today().isoformat(),
        )
        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return nueva_venta
