# restaurante_app - Semana 15

**Estudiante: Joseph Bolívar Montoya Arias**

## Tema

Conceptos fundamentales de manejo de eventos con Tkinter.

## Propósito de la Semana 15

A partir de la interfaz gráfica construida en la Semana 14, esta
entrega **continúa la evolución** de `restaurante_app` sin
reconstruirla desde cero: se conservan el inicio de sesión, la
navegación, la gestión de productos y la consulta de usuarios que ya
funcionaban.

El propósito central es comprender el **fundamento del manejo de
eventos**: cómo una acción del usuario (hacer clic) dispara, mediante
un botón asociado a `command=`, un **callback** en la interfaz que
delega la operación al servicio, persiste el resultado y actualiza lo
que el usuario ve.

```text
USUARIO
   ↓ realiza una accion
BOTON / COMPONENTE
   ↓ command=
CALLBACK
   ↓
RestauranteServicio
   ↓
PERSISTENCIA (ventas.json)
   ↓
RESPUESTA EN LA INTERFAZ (Treeview actualizado)
```

Para practicar este flujo se usó como contexto la operación de
**venta**, que relaciona un **Usuario** con un **Producto** en una
**fecha**.

## Qué NO se trabaja todavía

Tal como en el proyecto docente, esta semana **no** se implementan
eventos avanzados:

- `bind()`
- doble clic
- eventos de teclado o mouse
- `<<TreeviewSelect>>`
- carga automática desde tablas / selección reactiva de filas

Estos conceptos quedan para la siguiente semana de manejo de eventos.
Tampoco se agrega facturación, carrito de compras ni control avanzado
de inventario: la venta es una relación simple para demostrar el
fundamento del evento, no un sistema comercial completo.

## Estructura del proyecto

```
restaurante_app/
├── assets/
│   ├── icons/
│   │   ├── home.png / home_blanco.png
│   │   ├── productos.png / productos_blanco.png
│   │   ├── usuarios.png / usuarios_blanco.png
│   │   ├── ventas.png / ventas_blanco.png
│   │   ├── logout.png / logout_blanco.png
│   │   ├── add.png / add_blanco.png
│   │   ├── search.png / search_blanco.png
│   │   ├── edit.png / edit_blanco.png
│   │   ├── delete.png / delete_blanco.png
│   │   └── clean.png / clean_blanco.png
│   ├── logo_restaurante.png
│   └── logo_encabezado.png
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── estilos.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

## Novedades de esta semana

### 1. Modelo `Venta`

`modelos/venta.py` relaciona `usuario_id` + `producto_codigo` + `fecha`
(con un `identificador` propio, generado automáticamente). Usa
`@property` para validar que ningún campo llegue vacío, siguiendo el
mismo patrón que `Producto` y `Usuario`.

### 2. `RestauranteServicio` ampliado

- Carga y persiste `ventas.json` (`cargar_datos()`, `guardar_ventas()`).
- `buscar_usuario(identificacion)`: nueva búsqueda, necesaria para
  relacionar la venta con un usuario existente.
- `generar_identificador_venta()`: genera identificadores secuenciales
  (`V001`, `V002`, ...) a partir de las ventas ya cargadas, por lo que
  la secuencia **no se reinicia** al reabrir la aplicación.
- `registrar_venta(usuario_id, producto_codigo)`: valida que ambos
  campos vengan seleccionados y que el usuario y el producto existan
  antes de crear la `Venta` y guardarla. Todas las reglas viven aquí,
  **no** en la interfaz.

### 3. Sección **Ventas** en la interfaz

- Dos `ttk.Combobox` en modo `readonly` para elegir un **usuario** y un
  **producto** ya registrados (evita escribir códigos a mano y errores
  de tipeo).
- Botón **Registrar venta** asociado con `command=self.registrar_venta`.
- El callback `registrar_venta()` obtiene la selección de los
  `Combobox`, delega el registro a `RestauranteServicio`, limpia la
  selección y refresca la tabla — sin contener reglas de negocio.
- Tabla `ttk.Treeview` con las ventas registradas (identificador,
  usuario, producto y fecha), con su `ttk.Scrollbar`.
- La barra de estado inferior ahora también muestra el total de ventas.

### 4. Carpeta `assets/` obligatoria: íconos y logo

Se agregó `assets/icons/` con 10 íconos (en versión oscura, para
botones de fondo claro, y blanca, para botones de color), generados en
la misma paleta visual del proyecto: `home`, `productos`, `usuarios`,
`ventas`, `logout`, `add`, `search`, `edit`, `delete` y `clean`.

- `ui/estilos.py` agrega `cargar_icono(nombre_base, blanco=False)`,
  que resuelve la ruta dentro de `assets/icons/`.
- `MainView.crear_boton(...)` es el único lugar donde se arma un botón
  con ícono: si el ícono existe, se agrega con `compound="left"`; si
  no existe, el botón se crea **solo con texto**, sin pasar `image=None`
  de forma explícita. Así, si falta un ícono en el equipo del
  profesor, la aplicación sigue funcionando sin errores.
- El logo del restaurante (`logo_restaurante.png` en el login y
  `logo_encabezado.png` en el encabezado) se conserva de la Semana 14.

## Componentes Tkinter utilizados

`Label`, `Entry`, `ttk.Combobox`, `ttk.Button` (con `command=`),
`ttk.Treeview`, `ttk.Scrollbar`, `messagebox`, `ttk.LabelFrame`,
`ttk.Style`.

## Persistencia

| Operación | Archivo(s) |
|---|---|
| Registrar / actualizar / eliminar producto | `productos.json` |
| Registrar venta | `ventas.json` |

Los tres archivos (`productos.json`, `usuarios.json`, `ventas.json`) se
cargan al iniciar la aplicación y se reconstruyen como objetos
(`Producto`, `Usuario`, `Venta`).

## Separación de responsabilidades

- **`ui/`**: captura la interacción del usuario y llama al servicio.
  **No** lee ni escribe JSON, y **no** valida reglas del restaurante.
- **`servicios/restaurante_servicio.py`**: concentra las validaciones
  (usuario/producto deben existir, campos no vacíos) y la persistencia.
- **`modelos/`**: cada clase valida sus propios datos con `@property`.

## Flujo funcional

```
Inicio de la aplicación
        ↓
LoginView
        ↓
Validación mediante RestauranteServicio
        ↓
MainView
        ↓
Navegación por las secciones del sistema
        ↓
Usuarios → consulta de información
        ↓
Productos → gestión (Registrar, Cargar, Actualizar, Eliminar)
        ↓
Ventas → selección de usuario + selección de producto
        ↓
Botón "Registrar venta"
        ↓
command= → callback registrar_venta()
        ↓
RestauranteServicio valida y registra la operación
        ↓
Persistencia en ventas.json
        ↓
Actualización de la tabla de ventas
        ↓
Respuesta visual al usuario (messagebox)
```

## Credenciales de demostración

Usuario: `admin` — Contraseña: `1234`

También puede usarse:

Usuario: `mesero` — Contraseña: `abcd`

