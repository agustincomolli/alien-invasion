import pygame, sys, os
from pygame.sprite import Sprite

class Alien(Sprite):
    """Representa una nave alienígena dentro de su flota."""

    def __init__(self, config_juego, pantalla):
        """Inicializar la nave enemiga y establecer su posición."""
        super(Alien, self).__init__()
        self.config_juego = config_juego
        self.pantalla = pantalla

        # Cargar la imagen de la nave y establecer el atributo rect.
        self.image = pygame.image.load(resource_path("imagenes/alien.png"))
        self.rect = self.image.get_rect()

        # Empezar el nuevo alienigena en la parte cercana a la esquina
        # superior izquierda.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Guardar la posición exacta del alien.
        self.x = float(self.rect.x)

    
    def dibujame(self):
        """Dibuja el alien en la posición correspondiente."""
        self.pantalla.blit(self.image, self.rect)

    
    def chequear_bordes(self):
        """Devuelve True si los aliens tocan los bordes de la pantalla."""
        pantalla_rect = self.pantalla.get_rect()
        if self.rect.right >= pantalla_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        """Mover aliens a la derecha."""
        self.x += (self.config_juego.factor_velocidad_alien *
                    self.config_juego.direccion_flota)
        self.rect.x = self.x


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
