class Producto:
    def __init__(self, codigo, nombre, categoria, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    @staticmethod
    def validar_texto(valor, campo):
        # Reutiliza una validacion basica para datos obligatorios de texto.
        if not valor or not str(valor).strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")

        return str(valor).strip()

    @staticmethod
    def validar_numero(valor, campo, permitir_negativo=False):
        # Reutiliza una validacion basica para datos numericos.
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError(f"El campo {campo} debe ser un numero valido.")

        if not permitir_negativo and numero < 0:
            raise ValueError(f"El campo {campo} no puede ser negativo.")

        return numero

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = self.validar_texto(valor, "codigo")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = self.validar_texto(valor, "categoria")

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = self.validar_numero(valor, "precio")

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        self._stock = int(self.validar_numero(valor, "stock"))
