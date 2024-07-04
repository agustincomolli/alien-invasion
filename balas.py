import pygame, sys, os
from pygame.sprite import Sprite

class Bala(Sprite):
    """Clase que maneja las balas disparadas desde la nave."""

    def __init__(self, config_juego, pantalla, nave):
        """Crear un objeto bala en la posición actual de la nave."""

        super().__init__()
        self.pantalla = pantalla

        # Crear un rectangulo para la bala y establecer su posición actual.
        self.rect = pygame.Rect(0, 0, config_juego.ancho_balas, 
            config_juego.alto_balas)
        self.rect.centerx = nave.rect.centerx
        self.rect.top = nave.rect.top

        # Almacenar la posición actual de la bala como valor decimal.
        self.y = float(self.rect.y)

        self.color = config_juego.color_balas
        self.factor_velocidad = config_juego.factor_velocidad_balas

        # Almacenar sonido de bala.
        self.sonido = pygame.mixer.Sound(resource_path("sonidos/laser_nave.wav"))

    
    # Tengo que usar el nombre en inglés porque pygame.sprite.Group.update()
    # llama al método update de todas las clases que están en el grupo.
    def update(self):
        """Mover la bala hacia arriba de la pantalla."""

        # Actualizar la posición decimal de la bala.
        self.y -= self.factor_velocidad
        # Actualizar la posición del rectángulo de la bala.
        self.rect.y = self.y
    

    def dibujar_bala(self):
        """Dibuja la bala en la pantalla."""

        pygame.draw.rect(self.pantalla, self.color, self.rect)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
