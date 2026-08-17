from PySide6.QtWidgets import (
    QPushButton,
    QMenu,
    QWidgetAction,
    QDoubleSpinBox,
    QLabel
)

from PySide6.QtCore import (
    Qt,
    Signal
)


class LedButton(QPushButton):

    fadeChanged = Signal(float)

    fadeToggled = Signal(bool)


    def __init__(self):

        super().__init__()

        self.activo = False

        self.fade_time = 1.50


        self.setFixedSize(
            18,
            18
        )


        self.setCursor(
            Qt.PointingHandCursor
        )


        self.actualizar()


    def actualizar(self):

        if self.activo:

            self.setStyleSheet("""
                QPushButton{
                    background:qradialgradient(
                        cx:0.5, cy:0.5,
                        radius:0.8,
                        fx:0.35, fy:0.35,
                        stop:0 #ff9cff,
                        stop:0.5 #c000ff,
                        stop:1 #500060
                    );

                    border:2px solid #c8a0ff;
                    border-radius:9px;
                }

                QPushButton:hover{
                    border:2px solid white;
                }
            """)

        else:

            self.setStyleSheet("""
                QPushButton{
                    background:qradialgradient(
                        cx:0.5, cy:0.5,
                        radius:0.8,
                        fx:0.35, fy:0.35,
                        stop:0 #8a8a8a,
                        stop:1 #303030
                    );

                    border:2px solid #666666;
                    border-radius:9px;
                }

                QPushButton:hover{
                    border:2px solid #aaaaaa;
                }
            """)


    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.activo = not self.activo


            self.actualizar()


            self.fadeToggled.emit(
                self.activo
            )


            return


        if event.button() == Qt.RightButton:

            self.menu_fade(
                event.globalPos()
            )

            return


        super().mousePressEvent(
            event
        )


    def menu_fade(self, posicion):

        menu = QMenu()


        display = QLabel()

        display.setAlignment(
            Qt.AlignCenter
        )

        display.setFixedSize(
            70,
            30
        )

        display.setStyleSheet("""
            QLabel {
                background-color: #071008;
                color: #39ff88;
                border: 2px solid #202820;
                border-radius: 3px;
                padding: 1px;
                font-family: "Courier New";
                font-size: 16px;
                font-weight: bold;
            }
        """)


        display.setText(
            f"{self.fade_time:04.2f}s"
        )


        spin = QDoubleSpinBox()


        spin.setDecimals(
            2
        )


        spin.setMinimum(
            0.10
        )


        spin.setMaximum(
            10.00
        )


        spin.setSingleStep(
            0.10
        )


        spin.setSuffix(
            " s"
        )


        spin.setValue(
            self.fade_time
        )


        def actualizar_display(valor):

            display.setText(
                f"{valor:04.2f}s"
            )

            self.cambiar_fade(
                valor
            )


        spin.valueChanged.connect(
            actualizar_display
        )


        accion_display = QWidgetAction(
            menu
        )


        accion_display.setDefaultWidget(
            display
        )


        menu.addAction(
            accion_display
        )


        accion_spin = QWidgetAction(
            menu
        )


        accion_spin.setDefaultWidget(
            spin
        )


        menu.addAction(
            accion_spin
        )


        menu.exec(
            posicion
        )


    def cambiar_fade(self, valor):

        self.fade_time = valor


        self.fadeChanged.emit(
            valor
        )
