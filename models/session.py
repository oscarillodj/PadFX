import json
import os

from audio.player import AudioPlayer


class Session:

    @staticmethod
    def guardar(archivo, pads):

        datos = {
            "version": 2,
            "volumen_master": AudioPlayer.volumen_master,
            "pads": []
        }


        for pad in pads:

            datos["pads"].append({
                "numero": pad.pad.numero,
                "nombre": pad.pad.nombre,
                "modo": pad.pad.modo,
                "ruta": pad.pad.ruta_archivo,
                "volumen": pad.pad.volumen,
                "fade_activo": pad.pad.fade_activo,
                "fade_time": pad.pad.fade_time
            })


        with open(
            archivo,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                datos,
                f,
                indent=4,
                ensure_ascii=False
            )


    @staticmethod
    def cargar(archivo, pads):

        if not os.path.exists(archivo):

            return


        with open(
            archivo,
            "r",
            encoding="utf-8"
        ) as f:

            datos = json.load(f)


        if isinstance(datos, list):

            datos_pads = datos
            volumen_master = 1.0

        else:

            datos_pads = datos.get(
                "pads",
                []
            )

            volumen_master = datos.get(
                "volumen_master",
                1.0
            )


        AudioPlayer.set_master_volume(
            volumen_master
        )


        for item in datos_pads:

            numero = item["numero"] - 1


            if 0 <= numero < len(pads):

                pad = pads[numero]


                pad.pad.nombre = item.get(
                    "nombre",
                    "VACÍO"
                )


                pad.pad.modo = item.get(
                    "modo",
                    "KILL"
                )


                pad.pad.ruta_archivo = item.get(
                    "ruta"
                )


                pad.pad.volumen = item.get(
                    "volumen",
                    1.0
                )


                pad.pad.fade_activo = item.get(
                    "fade_activo",
                    False
                )


                pad.pad.fade_time = item.get(
                    "fade_time",
                    1.50
                )


                pad.volumen_slider.setValue(
                    int(
                        pad.pad.volumen * 100
                    )
                )


                pad.fade_led.activo = (
                    pad.pad.fade_activo
                )


                pad.fade_led.actualizar()


                pad.actualizar_texto()
