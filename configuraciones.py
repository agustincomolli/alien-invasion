class Configuracion():
    """Clase que almacena todas las configuraciones del juego."""

    def __init__(self) -> None:
        """Inicializa las configuraciones del juego."""
        # Configuración de pantalla.
        self.pantalla_ancho = 1200
        self.pantalla_alto = 700
        self.color_fondo = (0, 0, 0)

        # Configuración de la nave.
        self.limite_naves = 2

        # Configuración de las balas.
        self.ancho_balas = 3
        self.alto_balas = 15
        self.color_balas = 249, 108, 17
        self.balas_permitidas = 3

        # Configuración de los alien.
        self.velocidad_bajada_flota = 15

        # Qué tan rápido se acelera el juego.
        self.escala_aceleracion = 1.1
        # Qué tan rápido aumentan los valores de los puntos alienígenas.
        self.escala_puntaje = 1.5

        self.inicializar_config_dinamica()


    def inicializar_config_dinamica(self):
        """Inicializa configuraciones que cambian a lo largo del juego."""
        self.factor_velocidad = 6
        self.factor_velocidad_balas = 9
        self.factor_velocidad_alien = 2
        # Direccion_flota en 1 representa la derecha, -1 la izquierda.
        self.direccion_flota = 1
        # Puntos por alien.
        self.puntos_alien = 10


    def aumentar_velocidad(self):
        """Aumentar la configuración de velocidad."""
        self.factor_velocidad *= self.escala_aceleracion
        self.factor_velocidad_balas *= self.escala_aceleracion
        self.factor_velocidad_alien *= self.escala_aceleracion
        self.puntos_alien = int(self.puntos_alien * self.escala_puntaje)
