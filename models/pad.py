import os


class Pad:

    def __init__(self, numero):

        self.numero = numero

        self.ruta_archivo = None

        self.nombre = "VACÍO"

        self.modo = "KILL"
        
        self.volumen = 1.0

        self.fade_activo = False

        self.fade_time = 1.50



    def cargar_archivo(self, ruta):

        self.ruta_archivo = ruta

        nombre = os.path.basename(ruta)

        self.nombre = os.path.splitext(nombre)[0]