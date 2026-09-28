import json
from pathlib import Path


class ArchivoServicio:
    def __init__(self, carpeta_datos):
        self.carpeta_datos = Path(carpeta_datos)

    def leer_json(self, nombre_archivo):
        ruta = self.carpeta_datos / nombre_archivo

        if not ruta.exists():
            return []

        with ruta.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def escribir_json(self, nombre_archivo, datos):
        ruta = self.carpeta_datos / nombre_archivo
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
