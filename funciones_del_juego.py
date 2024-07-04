import sys
import os
import pygame
import time

from balas import Bala
from alien import Alien
from boton import Boton
from time import sleep

musica = pygame.mixer.music

def empezar_juego(config_juego, estadisticas, barra_marcador, pantalla, 
    nave, aliens, balas):
    # Ocultar el cursosr del mouse.
    pygame.mouse.set_visible(False)
    # Reiniciar valores predeterminados del juego.
    estadisticas.reiniciar_estadisticas()
    config_juego.inicializar_config_dinamica()
    barra_marcador.preparar_marcador()
    barra_marcador.preparar_nivel()
    estadisticas.estado_juego = True
    # Vaciar la lista de aliens y balas.
    aliens.empty()
    balas.empty()
    # Crear una nueva flota de aliens y centrar la nave.
    crear_flota_alien(config_juego, pantalla, nave, aliens)
    nave.centrar_nave()
    musica.load(resource_path("sonidos/musica.ogg"))
    musica.play(-1)


def obtener_aliens_por_fila(config_juego, alien_ancho):
    """Determinar el número de aliens que entran en una fila."""
    
    # El espacio entre cada alienígena es igual al ancho de un alienígena.
    espacio_en_fila = config_juego.pantalla_ancho - 2 * alien_ancho
    aliens_por_fila = int(espacio_en_fila / (2 * alien_ancho))
    return aliens_por_fila


def obtener_cantidad_filas(config_juego, nave_altura, alien_altura):
    """Determina el número de filas de aliens que entran en la pantalla."""

    espacio_disponible = (config_juego.pantalla_alto - 
                            (3 * alien_altura) - (nave_altura + 40 ))
    numero_filas = int(espacio_disponible / (2 * alien_altura))
    return numero_filas

def crear_alien(config_juego, pantalla, aliens, numero_alien, numero_fila,
                aliens_por_fila):
    """Crear un alien y posicionarlo en la fila."""

    alien = Alien(config_juego, pantalla)
    alien_ancho = alien.rect.width
    
    # Establecer el eje X para centrar la fila de aliens en la pantalla.
    # Ancho que ocupan todos los aliens de la fila.
    posicion_inicial = alien_ancho * aliens_por_fila
    # Ancho que ocupan los espacios entre los aliens contando el espacio 
    # al inicio.
    posicion_inicial += alien_ancho * (aliens_por_fila + 1)
    # Obtener la posición inicial.
    posicion_inicial = (config_juego.pantalla_ancho - posicion_inicial)
    alien.x = posicion_inicial + 2 * alien_ancho * numero_alien
    # alien.x = alien_ancho + 2 * alien_ancho * numero_alien
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * numero_fila
    aliens.add(alien)


def crear_flota_alien(config_juego, pantalla, nave, aliens):
    """Crear una flota entera de aliens."""
    
    # Crea un alienígena y encuentra el número de alienígenas en una fila.
    alien = Alien(config_juego, pantalla)
    aliens_por_fila = obtener_aliens_por_fila(config_juego, alien.rect.width)
    filas_de_aliens = obtener_cantidad_filas(config_juego, nave.rect.height, 
                                            alien.rect.height)
    
    # Crear la flota de aliens.
    for numero_fila in range(filas_de_aliens):
        for numero_alien in range(aliens_por_fila):
            # Crear un alien y colocarlo en la fila.
            crear_alien(config_juego, pantalla, aliens, numero_alien, 
                        numero_fila, aliens_por_fila)

def disparar_balas(config_juego, pantalla, nave, balas):
    """Dispara una bala mientras no supere la cantidad permitida."""
    if len(balas) < config_juego.balas_permitidas:
        nueva_bala = Bala(config_juego, pantalla, nave)
        balas.add(nueva_bala)
        nueva_bala.sonido.play()


def chequear_eventos_tecla_presionada(evento, config_juego, estadisticas, 
    barra_marcador, pantalla, nave, aliens, balas):
    """Responder a las pulsaciones de teclas."""
    if evento.key == pygame.K_RIGHT:
        nave.moviendo_derecha = True
    elif evento.key == pygame.K_LEFT:
        nave.moviendo_izquierda = True
    elif evento.key == pygame.K_SPACE:
        disparar_balas(config_juego, pantalla, nave, balas)
    elif evento.key == pygame.K_j:
        empezar_juego(config_juego, estadisticas, barra_marcador, pantalla, 
            nave, aliens, balas)
    elif evento.key == pygame.K_s:
        # Salir del juego.
        sys.exit()

def chequear_evento_tecla_liberada(evento, nave):
    """Responder a la tecla liberada."""
    if evento.key == pygame.K_RIGHT:
        nave.moviendo_derecha = False
    elif evento.key == pygame.K_LEFT:
        nave.moviendo_izquierda = False


def chequear_eventos(config_juego, pantalla, estadisticas, barra_marcador, 
    nave, aliens, balas, boton_jugar, boton_salir):
    """Responda a las pulsaciones de teclas y eventos del mouse."""

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            # Activar el movimiento de la nave según la tecla
            # izquierda o derecha.
            chequear_eventos_tecla_presionada(evento, config_juego, 
                estadisticas, barra_marcador, pantalla, nave, aliens, balas)
        elif evento.type == pygame.KEYUP:
            # Desactivar el movimiento de la nave.
            chequear_evento_tecla_liberada(evento, nave)
        elif evento.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            chequear_botones(config_juego, pantalla, estadisticas, barra_marcador, 
                boton_jugar, boton_salir, nave, aliens, balas, mouse_x, mouse_y)


def chequear_botones(config_juego, pantalla, estadisticas, barra_marcador, 
    boton_jugar, boton_salir, nave, aliens, balas, mouse_x, mouse_y):
    """Empezar o salir del juego, según el botón presionado."""
    boton_jugar_presionado = boton_jugar.rect.collidepoint(mouse_x, mouse_y)
    boton_salir_presionado = boton_salir.rect.collidepoint(mouse_x, mouse_y)
    estado_juego = estadisticas.estado_juego
    # Si el juego está activo, deshabilitar el área de los botones.
    if boton_jugar_presionado and not estado_juego:
        empezar_juego(config_juego, estadisticas, barra_marcador, pantalla, 
            nave, aliens, balas)
    elif boton_salir_presionado and not estado_juego:
        sys.exit()


def actualizar_pantalla(config_juego, pantalla, estadisticas, barra_marcador, 
     nave, aliens, balas, boton_jugar, boton_salir):
    """Actualiza las imágenes en la pantalla y cambia a la nueva pantalla."""
    # Vuelva a dibujar la pantalla durante cada pasada por el bucle.
    fondo_pantalla = pygame.image.load(resource_path("imagenes/fondo.jpg"))
    pantalla.blit(fondo_pantalla, (0, 0))
    # Redibujar todas las balas que están entre la nave y los enemigos.
    for bala in balas.sprites():
        bala.dibujar_bala()
    nave.dibujame()
    aliens.draw(pantalla)

    # Dibujar marcador de puntos.
    barra_marcador.mostrar_puntaje()
    
    # Dibujar el botón Jugar sin el estado del juego es inactivo.
    if not estadisticas.estado_juego:
        boton_jugar.dibujar_boton()
        boton_salir.dibujar_boton()

    # Hacer visible la pantalla dibujada más recientemente.
    pygame.display.flip()


def chequear_impacto_balas(config_juego, pantalla, estadisticas,  
        barra_marcador, nave, aliens, balas):
    """Responder a las colisiones de las balas con los aliens."""
    # Compruebe si hay balas que hayan alcanzado a los extraterrestres.
    # Si es así, deshazte de la bala y del alienígena.
    colisiones = pygame.sprite.groupcollide(balas, aliens, True, True)
    explosion_alien = pygame.mixer.Sound(
            resource_path("sonidos/explosion_alien.wav"))

    # Calcular los puntos por los aliens derribados.
    if colisiones:
        for aliens in colisiones.values():
            explosion_alien.play()
            estadisticas.puntaje += config_juego.puntos_alien
        barra_marcador.preparar_marcador()

    if len(aliens) == 0:
        empezar_nuevo_nivel(config_juego, pantalla, estadisticas, 
            barra_marcador, nave, aliens, balas)

def empezar_nuevo_nivel(config_juego, pantalla, estadisticas, barra_marcador, 
        nave, aliens, balas):
    """Limpia la pantalla y sube de nivel."""
    # Destruir las balas existentes y crear una nueva flota.
    balas.empty()
    config_juego.aumentar_velocidad()
    crear_flota_alien(config_juego, pantalla, nave, aliens)
    # Incrementar el nivel.
    estadisticas.nivel += 1
    barra_marcador.preparar_nivel()


def actualizar_balas(config_juego, pantalla, estadisticas, barra_marcador, 
    nave, aliens, balas):
    """Actualizar la posición de las balas y eliminar las bajas viejas."""
    balas.update()
    # Eliminar las balas que desaparecieron de la pantalla.
    for bala in balas.copy():
        if bala.rect.bottom <=50:
            balas.remove(bala)
    
    chequear_impacto_balas(config_juego, pantalla, estadisticas, barra_marcador, 
        nave, aliens, balas)


def cambiar_direccion_flota(config_juego, aliens):
    """Bajar toda la flota y cambiar su dirección."""
    for alien in aliens.sprites():
        alien.rect.y += config_juego.velocidad_bajada_flota
    
    config_juego.direccion_flota *= -1


def chequear_bordes_flota(config_juego, aliens):
    """Responder apropiadamente si un alien alcanza el borde."""
    for alien in aliens.sprites():
        if alien.chequear_bordes():
            cambiar_direccion_flota(config_juego, aliens)
            break


def destruir_nave(config_juego, estadisticas, pantalla, nave, aliens, balas):
    """Responder cuando la nave es alcanzada por un alien."""
    nave.explotar()
    reiniciar_nivel(config_juego, pantalla, nave, aliens, balas)
    if estadisticas.naves_restantes > 0:
        # Reducir el número de las naves que quedan.
        estadisticas.naves_restantes -= 1
    else:
        terminar_juego(config_juego, estadisticas, pantalla)


def terminar_juego(config_juego, estadisticas, pantalla):
    """Mostrar un cartel y sonido de fin de juego y guardar el record."""
    with open("record.txt", "w") as archivo:
        archivo.write(str(estadisticas.record))
    # Hacer visible el cursor del mouse.
    pygame.mouse.set_visible(True)
    estadisticas.estado_juego = False
    musica.stop()
    musica.load(resource_path("sonidos/juego_terminado.ogg"))
    musica.play()
    dibujar_juego_terminado(config_juego, pantalla)


def reiniciar_nivel(config_juego, pantalla, nave, aliens, balas):
    """Reiniciar el mismo nivelen que quedó el jugador."""
    # Limpiar la lista de aliens y balas.
    aliens.empty()
    balas.empty()
    # Crear una nueva flota y centrar la nave.
    crear_flota_alien(config_juego, pantalla, nave, aliens)
    nave.image = pygame.image.load(resource_path("imagenes/nave.png"))
    nave.centrar_nave()


def dibujar_juego_terminado(config_juego, pantalla):
    """Dibuja un cartel para finalizar el juego."""
    cartel = Boton(config_juego, pantalla, "¡Juego terminado!")
    cartel.color_boton = (140, 3, 3) # Rojo
    cartel.color_texto = (255, 247, 3) # Amarillo
    cartel.ancho = 600
    cartel.alto = 200
    # Establecer las dimensiones del cartel y centrarlo.
    cartel.rect = pygame.Rect(0, 0, cartel.ancho, cartel.alto)
    cartel.rect.center = cartel.pantalla_rect.center
    cartel.preparar_mensaje("¡Juego terminado!")
    cartel.dibujar_boton()
    pygame.display.flip()
    # Pausar el juego 4 segundos
    sleep(5)


def chequear_alien_abajo(config_juego, estadisticas, pantalla, nave, aliens, balas):
    """Chequear si un alien ha llegado al fondo de la pantalla."""
    pantalla_rect = pantalla.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= pantalla_rect.bottom:
            # Tratar esto como si la nave hubiese sido destruída.
            destruir_nave(config_juego, estadisticas, pantalla, nave, 
                aliens, balas)
            break


def actualizar_aliens(config_juego, estadisticas, pantalla, nave, aliens, balas):
    """
    Chequear si la flota está en los bordes y
    actualizar las posiciones de los aliens.
    """
    chequear_bordes_flota(config_juego, aliens)
    aliens.update()

    # Buscar coliciones entre los aliens y la nave.
    if pygame.sprite.spritecollideany(nave, aliens):
        destruir_nave(config_juego, estadisticas, pantalla, nave, aliens, balas)
    
    # Buscar aliens que hayan llegado a la parte inferior de la pantalla.
    chequear_alien_abajo(config_juego, estadisticas, pantalla, nave, 
        aliens, balas)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
