import sys
from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from midi.controller import MidiController


app = QApplication(sys.argv)

ventana = MainWindow()

midi = MidiController()


def recibir_pad(numero):

    print("ACTIVANDO PAD:", numero + 1)

    ventana.activar_pad_midi(numero)


midi.pad_pressed.connect(recibir_pad)


ventana.show()

sys.exit(app.exec())