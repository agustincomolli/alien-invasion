import pygame, sys, os
import pygame.font

from pygame.sprite import Group
from nave import Nave

class Marcador():
    """Una clase para mostrar información."""

    def __init__(self, config_juego, pantalla, estadisticas):
        """Inicializar atributos de registro de puntajes."""

        self.pantalla = pantalla
        self.pantalla_rect = pantalla.get_rect()
        self.config_juego = config_juego
        self.estadisticas = estadisticas

        # Color de fuente para mostrar información.
        self.color_texto = (255, 255, 255)
        self.fuente = pygame.font.SysFont("Arial", 18, True)

        # Preparar el marcador inicial.
        self.preparar_marcador()
        self.preparar_nivel()


    def preparar_marcador(self):
        """Convertir la puntuación en una imagen renderizada."""

        # Redondear para arriba los puntajes para que vayan de 10 en 10.
        puntaje_redondeado = int(round(self.estadisticas.puntaje, -1))
        # Si el puntaje es mayor al record, establecer nuevo record.
        if puntaje_redondeado > self.estadisticas.record:
            self.estadisticas.record = puntaje_redondeado
        # Mostrar puntos separadores de miles, primerp mostrando las comas
        # predeterminadas de Python y después reemplazándolas por el .
        puntaje_texto = "{:,}".format(puntaje_redondeado).replace(",", ".")
        # Agregar el record.
        puntaje_texto += " | {:,}".format(
            self.estadisticas.record).replace(",", ".")
        # Convertir el texto en imagen.
        self.puntaje_imagen = self.fuente.render(puntaje_texto, True, 
            self.color_texto, self.config_juego.color_fondo)

        # Mostrar el puntaje arriba en el centro de la pantalla.
        self.puntaje_rect = self.puntaje_imagen.get_rect()
        self.puntaje_rect.centerx = self.pantalla_rect.centerx
        self.puntaje_rect.top = 10


    def dibujar_vidas(self):
        """Poner imagen para saber la cantidad de vidas que quedan."""

        vidas = pygame.image.load(resource_path("imagenes/nave.png"))
        # Reducir imagen.
        imagen_vidas = pygame.transform.scale(vidas, (24, 24))
        # Marcar la posición inicial.
        posicion_x = 10
        for i in range(self.estadisticas.naves_restantes):
            self.pantalla.blit(imagen_vidas, [posicion_x, 8])
            # Correr la posición de la imagen siguiente y darle un espacio
            # de 5 pixeles entre imágenes.
            posicion_x += imagen_vidas.get_width() + 5


    def preparar_nivel(self):
        """Convertir el nivel en una imagen renderizada."""

        texto_nivel = "Nivel: " + str(self.estadisticas.nivel)
        self.nivel_imagen = self.fuente.render(texto_nivel, True,
            self.color_texto, self.config_juego.color_fondo)

        # Mostrar el puntaje arriba en el centro de la pantalla.
        self.nivel_rect = self.puntaje_imagen.get_rect()
        self.nivel_rect.right = self.pantalla_rect.right - 60   
        self.nivel_rect.top = 10


    def mostrar_puntaje(self):
        """Dibuja el puntaje en la pantalla."""
        self.pantalla.blit(self.puntaje_imagen, self.puntaje_rect)
        self.pantalla.blit(self.nivel_imagen, self.nivel_rect)
        self.dibujar_vidas()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
