import mido
from PySide6.QtCore import QObject, Signal


class MidiController(QObject):

    pad_pressed = Signal(int)

    def __init__(self):
        super().__init__()

        self.port = None
        self.conectar()


    def conectar(self):

        dispositivos = mido.get_input_names()

        for dispositivo in dispositivos:

            if "JP-Mini" in dispositivo:

                self.port = mido.open_input(dispositivo)

                print("MIDI conectado:", dispositivo)

                break


        if self.port:

            self.port.callback = self.recibir

        else:

            print("No se encontró controlador MIDI")



    def recibir(self, mensaje):

        if mensaje.type == "note_on" and mensaje.velocity > 0:

            nota = mensaje.note

            # JP-Mini usa notas 36-51
            pad_original = nota - 36


            # Corrige orientación física del JP-Mini
            mapa = [
                12, 13, 14, 15,
                8,  9,  10, 11,
                4,  5,  6,  7,
                0,  1,  2,  3
            ]


            if 0 <= pad_original < 16:

                pad = mapa[pad_original]

                print("MIDI -> PAD", pad + 1)

                self.pad_pressed.emit(pad)