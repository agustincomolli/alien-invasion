import pygame

from pygame.sprite import Group

from configuraciones import Configuracion
from nave import Nave
from alien import Alien
from estadisticas import Estadistica_Juego
from marcador import Marcador
from boton import Boton
from funciones_del_juego import resource_path

import funciones_del_juego

def ejecutar_juego():
    """Ejecuta el juego"""

    # Inicializa el juego y crea el objeto pantalla.
    pygame.init()
    config_juego = Configuracion()
    pantalla = pygame.display.set_mode(
        (config_juego.pantalla_ancho, config_juego.pantalla_alto)
        )
    pygame.display.set_caption("Invasión Alienígena")
    icono = pygame.image.load(resource_path("imagenes/nave.png"))
    pygame.display.set_icon(icono)

    # Crear el botón de "Jugar"
    boton_jugar = Boton(config_juego, pantalla, "Jugar")
    boton_jugar.color_boton = (0, 0, 0)
    boton_jugar.rect.top -= boton_jugar.alto
    boton_jugar.preparar_mensaje("Jugar")

    # Crear el botón de "Salir"
    boton_salir = Boton(config_juego, pantalla, "Salir")
    boton_salir.color_boton = (140, 3, 3)
    boton_salir.rect.top += 50
    boton_salir.preparar_mensaje("Salir")

    # Crear la instancia que va a guardar las estadísticas del juego.
    estadisticas = Estadistica_Juego(config_juego)
    barra_marcador = Marcador(config_juego, pantalla, estadisticas)

    # Crear la nave, el grupo de balas y el grupo de aliens.
    nave = Nave(config_juego, pantalla)
    balas = Group()
    aliens = Group()

    # Crear la flotilla de aliens.
    funciones_del_juego.crear_flota_alien(config_juego, pantalla, nave, aliens)

    # Empieza el bucle principal del juego.
    while True:
        # Vigilar eventos de teclado y mouse.
        funciones_del_juego.chequear_eventos(config_juego, pantalla, 
            estadisticas, barra_marcador, nave, aliens, balas, boton_jugar, 
            boton_salir)

        if estadisticas.estado_juego:
            nave.actualizar()
            funciones_del_juego.actualizar_balas(config_juego, pantalla, 
                estadisticas, barra_marcador, nave, aliens, balas)
            funciones_del_juego.actualizar_aliens(config_juego, estadisticas, 
                pantalla, nave, aliens, balas)
        
        funciones_del_juego.actualizar_pantalla(config_juego, pantalla, 
            estadisticas, barra_marcador, nave, aliens, balas, boton_jugar, boton_salir)

ejecutar_juego()
