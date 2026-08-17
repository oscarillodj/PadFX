import os

from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QFileDialog,
    QMenu,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QLabel
)

from PySide6.QtCore import Qt, QTimer

from models.pad import Pad
from audio.player import AudioPlayer
from gui.widgets.led_button import LedButton



class PadWidget(QWidget):

    def __init__(self, numero):

        super().__init__()

        self.pad = Pad(numero)

        self.modo_global = "SAMPLE"

        self.activo = False

        self.audio = AudioPlayer()


        self.timer_estado = QTimer()

        self.timer_estado.timeout.connect(
            self.actualizar_estado_audio
        )

        self.timer_estado.start(
            100
        )


        self.setMinimumSize(
            150,
            130
        )


        self.setMinimumSize(
            150,
            130
        )


        self.crear_interfaz()

        self.actualizar_texto()

        self.actualizar_color()



    def crear_interfaz(self):

        layout_principal = QHBoxLayout()

        layout_principal.setContentsMargins(
            5,
            5,
            5,
            5
        )


        columna = QVBoxLayout()


        self.fade_led = LedButton()


        self.fade_led.activo = self.pad.fade_activo


        self.fade_led.fadeChanged.connect(
            self.actualizar_tiempo_fade
        )

        self.fade_led.fadeToggled.connect(
            self.activar_fade
        )

        columna.addWidget(
            self.fade_led,
            alignment=Qt.AlignLeft
        )


        self.boton = QPushButton()


        self.boton.setMinimumSize(
            120,
            105
        )


        self.boton.clicked.connect(
            self.activar
        )


        columna.addWidget(
            self.boton
        )


        layout_principal.addLayout(
            columna
        )



        self.volumen_slider = QSlider(
            Qt.Vertical
        )

        columna_volumen = QVBoxLayout()


        self.display_volumen = QLabel()

        self.display_volumen.setAlignment(
            Qt.AlignCenter
        )

        self.display_volumen.setFixedSize(
            35,
            15
        )

        self.display_volumen.setStyleSheet("""
            QLabel {
                background-color: #071008;
                color: #39ff88;
                border: 2px solid #202820;
                border-radius: 3px;
                padding: 1px;
                font-family: "Courier New";
                font-size: 15px;
                font-weight: bold;
            }
        """)


        self.volumen_slider = QSlider(
            Qt.Vertical
        )


        self.volumen_slider.setRange(
            0,
            100
        )


        self.volumen_slider.setValue(
            int(self.pad.volumen * 100)
        )


        self.volumen_slider.setFixedHeight(
            100
        )


        self.volumen_slider.valueChanged.connect(
            self.cambiar_volumen_pad
        )


        columna_volumen.addWidget(
            self.display_volumen,
            alignment=Qt.AlignCenter
        )


        columna_volumen.addWidget(
            self.volumen_slider,
            alignment=Qt.AlignCenter
        )


        layout_principal.addLayout(
            columna_volumen
        )


        self.actualizar_display_volumen()


        layout_principal.addWidget(
            self.volumen_slider
        )


        self.setLayout(
            layout_principal
        )



    def cambiar_modo(self, modo):

        self.modo_global = modo

        self.actualizar_texto()



    def actualizar_texto(self):

        if self.modo_global == "SYNTH":

            nombres = [
                "C3", "D3", "E3", "F3",
                "G3", "A3", "B3", "C4",
                "D4", "E4", "F4", "G4",
                "♯", "♭", "⚡", "🌊"
            ]


            texto = (
                f"🛸\n"
                f"{nombres[self.pad.numero-1]}\n"
                f"[SYNTH]"
            )


        else:

            if self.pad.ruta_archivo:

                nombre = os.path.basename(
                    self.pad.ruta_archivo
                )

                nombre = os.path.splitext(
                    nombre
                )[0]

            else:

                nombre = self.pad.nombre


            if len(nombre) > 12:

                nombre = nombre[:12] + "..."


            texto = (
                f"🎵\n"
                f"{nombre}\n"
                f"[{self.pad.modo}]"
            )


        self.boton.setText(
            texto
        )


    def activar(self):

        if self.modo_global == "SYNTH":

            print(
                "SYNTH:",
                self.pad.numero
            )

            return


        if not self.pad.ruta_archivo:

            return


        reproduciendo = (
            self.audio.esta_reproduciendo()
        )


        if reproduciendo:


            if self.pad.fade_activo:


                self.audio.fade_out(
                    self.pad.fade_time
                )

            else:

                self.audio.detener()

        else:

            self.reproducir_sonido()



    def reproducir_sonido(self):

        if self.pad.modo == "LOOP":

            self.audio.reproducir_loop(
                self.pad.ruta_archivo,
                self.pad.volumen
            )

        else:

            self.audio.reproducir(
                self.pad.ruta_archivo,
                self.pad.volumen
            )



    def menu_contextual(self, posicion):

        menu = QMenu()


        cargar = menu.addAction(
            "🎵 Cargar sonido..."
        )


        menu.addSeparator()


        kill = menu.addAction(
            "⚡ Modo KILL"
        )


        play = menu.addAction(
            "▶ Modo PLAY"
        )


        loop = menu.addAction(
            "🔁 Modo LOOP"
        )


        accion = menu.exec(
            self.mapToGlobal(posicion)
        )


        if accion == cargar:

            self.cargar_sonido()


        elif accion == kill:

            self.pad.modo = "KILL"

            self.actualizar_texto()


        elif accion == play:

            self.pad.modo = "PLAY"

            self.actualizar_texto()


        elif accion == loop:

            self.pad.modo = "LOOP"

            self.actualizar_texto()



    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:

            if self.modo_global == "SAMPLE":

                self.menu_contextual(
                    event.pos()
                )

            return


        super().mousePressEvent(event)



    def cargar_sonido(self):

        archivo, _ = QFileDialog.getOpenFileName(

            self,

            "Seleccionar sonido",

            "",

            "Audio (*.wav *.mp3 *.ogg)"
        )


        if archivo:

            self.pad.cargar_archivo(
                archivo
            )

            self.actualizar_texto()



    def actualizar_color(self):

        if self.activo:

            self.boton.setStyleSheet("""
                QPushButton{
                    background:#1ed760;
                    color:white;
                    font-size:18px;
                    font-weight:bold;
                    border-radius:20px;
                }
            """)


        else:

            self.boton.setStyleSheet("""
                QPushButton{
                    background:#242424;
                    color:white;
                    font-size:18px;
                    font-weight:bold;
                    border-radius:20px;
                }
            """)



    def actualizar_tiempo_fade(self, valor):

        self.pad.fade_time = valor

    def actualizar_display_volumen(self):

        valor = int(
            self.pad.volumen * 100
        )

        self.display_volumen.setText(
            f"{valor:03d}"
        )

    def cambiar_volumen_pad(self, valor):

        self.pad.volumen = valor / 100


        self.actualizar_display_volumen()


        self.audio.set_volume(
            self.pad.volumen
        )
    def fade_audio(self):

        if self.pad.fade_activo:

            self.audio.fade_out(
                self.pad.fade_time
            )

            self.activo = False

            self.actualizar_color()
            
    def activar_fade(self, activo):

        self.pad.fade_activo = activo
        
    def actualizar_estado_audio(self):

        if self.audio.channel:

            self.activo = (
                self.audio.channel.get_busy()
            )

        else:

            self.activo = False


        if not self.activo:

            self.audio.channel = None


        self.actualizar_color()