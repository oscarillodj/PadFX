from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QDial
)

from PySide6.QtCore import Qt

from gui.pad_widget import PadWidget
from models.session import Session
from audio.player import AudioPlayer


VERSION = "0.6"


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            f"PadFX v{VERSION}"
        )

        self.resize(
            900,
            750
        )

        self.setStyleSheet("""
            QMainWindow {
                background-color:#121212;
            }

            QLabel {
                color:white;
                font-size:16px;
            }

            QPushButton {
                background:#242424;
                color:white;
                font-size:16px;
                border-radius:12px;
                padding:10px;
            }

            QPushButton:hover {
                background:#333333;
            }

            QDial {
                background:#181818;
            }
        """)


        central = QWidget()

        self.setCentralWidget(
            central
        )


        layout = QVBoxLayout()

        central.setLayout(
            layout
        )


        self.grid = QGridLayout()

        self.grid.setSpacing(
            15
        )


        self.pads = []


        for fila in range(4):

            for columna in range(4):

                numero = fila * 4 + columna + 1

                boton = PadWidget(
                    numero
                )

                self.grid.addWidget(
                    boton,
                    fila,
                    columna
                )

                self.pads.append(
                    boton
                )


        layout.addLayout(
            self.grid
        )


        inferior = QHBoxLayout()


        botones = QVBoxLayout()


        guardar = QPushButton(
            "💾 Guardar sesión"
        )


        abrir = QPushButton(
            "📂 Abrir sesión"
        )


        guardar.clicked.connect(
            self.guardar_sesion
        )

        abrir.clicked.connect(
            self.abrir_sesion
        )


        botones.addWidget(
            guardar
        )

        botones.addWidget(
            abrir
        )


        inferior.addLayout(
            botones
        )


        inferior.addStretch()


        volumen_box = QVBoxLayout()


        titulo = QLabel(
            "MASTER"
        )


        titulo.setAlignment(
            Qt.AlignCenter
        )


        self.master = QDial()


        self.master.setRange(
            0,
            100
        )


        self.master.setValue(
            100
        )


        self.master.setWrapping(
            False
        )


        self.master.setNotchesVisible(
            True
        )


        self.master.setFixedSize(
            160,
            160
        )


        self.master.valueChanged.connect(
            self.cambiar_volumen
        )


        volumen_box.addWidget(
            titulo
        )


        volumen_box.addWidget(
            self.master
        )


        inferior.addLayout(
            volumen_box
        )


        layout.addLayout(
            inferior
        )


        self.estado = QLabel(
            "MIDI: Esperando controlador..."
        )


        layout.addWidget(
            self.estado
        )


        self.marca = QLabel(
            f"PadFX v{VERSION}  |  Developed by OscarilloDJ"
        )


        self.marca.setAlignment(
            Qt.AlignCenter
        )


        self.marca.setStyleSheet("""
            QLabel {
                color:#777777;
                font-size:14px;
                font-style:italic;
            }
        """)


        layout.addWidget(
            self.marca
        )


    def activar_pad_midi(self, numero):

        if 0 <= numero < len(self.pads):

            self.pads[numero].activar()



    def cambiar_modo(self, modo):

        print(
            "CAMBIO DE MODO:",
            modo
        )


        for pad in self.pads:

            pad.cambiar_modo(
                modo
            )



    def cambiar_volumen(self, valor):

        volumen = valor / 100


        AudioPlayer.set_master_volume(
            volumen
        )


        self.estado.setText(
            f"Master: {valor}%"
        )



    def midi_conectado(self, nombre):

        self.estado.setText(
            f"MIDI conectado: {nombre}"
        )



    def guardar_sesion(self):

        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar sesión",
            "",
            "PadFX (*.padfx)"
        )


        if archivo:

            Session.guardar(
                archivo,
                self.pads
            )


            self.estado.setText(
                "Sesión guardada"
            )



    def abrir_sesion(self):

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir sesión",
            "",
            "PadFX (*.padfx)"
        )


        if archivo:

            Session.cargar(
                archivo,
                self.pads
            )


            self.master.setValue(
                int(
                    AudioPlayer.volumen_master * 100
                )
            )


            self.estado.setText(
                "Sesión cargada"
            )