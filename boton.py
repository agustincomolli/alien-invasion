import pygame

class Boton():
    
    def __init__(self, config_juego, pantalla, mensaje):
        """Inicializar los atributos del botón."""

        self.pantalla = pantalla
        self.pantalla_rect = pantalla.get_rect()

        # Establecer las dimensiones y las porpiedades del botón.
        self.x, self.y = 0, -150
        self.ancho, self.alto = 200, 50
        self.color_boton = (0, 255, 0)
        self.color_texto = (255, 255, 255)
        self.fuente = pygame.font.SysFont(None, 48)

        # Construir el botón y centrarlo en la pantalla.
        self.rect = pygame.Rect(0, 0, self.ancho, self.alto)
        self.rect.center = self.pantalla_rect.center

        # El mensaje del botón solo debe prepararse una vez.
        self.preparar_mensaje(mensaje)


    def preparar_mensaje(self, mensaje):
        """Convertir el mensaje en una imagen y centrarla en el botón."""

        self.imagen_mensaje = self.fuente.render(mensaje, True, 
            self.color_texto, self.color_boton)
        self.imagen_mensaje_rect = self.imagen_mensaje.get_rect()
        self.imagen_mensaje_rect.center = self.rect.center

    
    def dibujar_boton(self):
        """Dibuja un botón y su mensaje."""

        self.pantalla.fill(self.color_boton, self.rect)
        self.pantalla.blit(self.imagen_mensaje, self.imagen_mensaje_rect)