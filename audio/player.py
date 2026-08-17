import pygame


class AudioPlayer:

    volumen_master = 1.0

    canales_activos = []


    def __init__(self):

        if not pygame.mixer.get_init():

            pygame.mixer.init()


        self.sound = None

        self.channel = None


    def reproducir(self, archivo, volumen_pad=1.0):

        self.sound = pygame.mixer.Sound(
            archivo
        )


        self.channel = self.sound.play()


        if self.channel:

            AudioPlayer.canales_activos.append(
                self.channel
            )


            volumen_final = (
                volumen_pad *
                AudioPlayer.volumen_master
            )


            self.channel.set_volume(
                volumen_final
            )


    def reproducir_loop(self, archivo, volumen_pad=1.0):

        self.sound = pygame.mixer.Sound(
            archivo
        )


        self.channel = self.sound.play(
            loops=-1
        )


        if self.channel:

            AudioPlayer.canales_activos.append(
                self.channel
            )


            volumen_final = (
                volumen_pad *
                AudioPlayer.volumen_master
            )


            self.channel.set_volume(
                volumen_final
            )


    def detener(self):

        if self.channel:

            self.channel.stop()


    def fade_out(self, segundos=3):

        if not self.channel:

            return


        if not self.channel.get_busy():

            return


        pasos = 30


        volumen_inicial = (
            self.channel.get_volume()
        )


        for paso in range(
            pasos,
            -1,
            -1
        ):

            volumen = (
                volumen_inicial *
                paso /
                pasos
            )


            self.channel.set_volume(
                volumen
            )


            pygame.time.wait(
                int(
                    (segundos * 1000) /
                    pasos
                )
            )


        self.channel.stop()


    def esta_reproduciendo(self):

        if self.channel:

            return self.channel.get_busy()


        return False


    def set_volume(self, volumen_pad):

        if not self.channel:

            return


        if not self.channel.get_busy():

            return


        volumen_final = (
            volumen_pad *
            AudioPlayer.volumen_master
        )


        self.channel.set_volume(
            volumen_final
        )


    @classmethod
    def set_master_volume(cls, valor):

        cls.volumen_master = valor


        for canal in cls.canales_activos:

            if canal.get_busy():

                canal.set_volume(
                    valor
                )


