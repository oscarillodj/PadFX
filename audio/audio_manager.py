from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QSoundEffect


class AudioManager:

    def __init__(self):

        self.player = QSoundEffect()

        self.player.setVolume(1.0)

        self.reproduciendo = False

        self.player.playingChanged.connect(self.actualizar_estado)


    def actualizar_estado(self):

        self.reproduciendo = self.player.isPlaying()


    def reproducir_o_detener(self, ruta):

        if self.player.isPlaying():

            self.player.stop()
            self.reproduciendo = False
            return

        self.player.setSource(QUrl.fromLocalFile(ruta))

        self.player.play()

        self.reproduciendo = True