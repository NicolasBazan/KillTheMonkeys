#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random

TIEMPO = 6
fin_de_juego = False

pilas = pilasengine.iniciar()
# Usar un fondo estándar
pilas.fondos.Pasto()
# Añadir un marcador
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.negro)
puntos.magnitud = 30
# Añadir el conmutador de Sonido
pilas.actores.Sonido()

# Variables y Constantes
balas_simples = pilas.actores.Bala
monos = []

# Funciones
def mono_destruido(disparo,enemigo):
    enemigo.eliminar()
    disparo.eliminar()
    efecto=random.uniform(1,3)
    puntos.aumentar()
    puntos.escala=(3,efecto),.25
    a=monos.index(enemigo)
    del monos[a]
    

def game_over(torreta, enemigo):
    global fin_de_juego
    enemigo.sonreir()
    torreta.eliminar()
    texto1=pilas.actores.Texto("Conseguiste %d puntos"%(puntos.obtener()))
    texto1.y=-150
    texto1.definir_color(pilas.colores.rojo)
    texto2=pilas.actores.Texto("GAME OVER")
    texto2.definir_color(pilas.colores.rojo)
    texto2.y=150
    puntos.eliminar()
    fin_de_juego=True
def crear_mono():
    # Crear un enemigo nuevo
    enemigo = pilas.actores.Mono()
    bonito=random.uniform(0.25,0.75)
    enemigo.escala=(1,bonito),.25
    # Hacer que se aparición sea con un efecto bonito
    ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
    enemigo.radio_de_colision = bonito*50
    # Dotarle de la habilidad de que explote al ser alcanzado por un disparo
    enemigo.aprender(pilas.habilidades.PuedeExplotar)
    # Situarlo en una posición al azar, no demasiado cerca del jugador
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)
    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180
    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180
    enemigo.x = x
    enemigo.y = y
    duracion = 1 +random.random()*4
    pilas.utils.interpolar(enemigo, 'x', 0, duracion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion)
    monos.append(enemigo)
    #Inicio de las estrellas
    if random.randrange(0,20)>15:
		if (torreta.municion!=pilasengine.actores.Misil):
			estrella=pilas.actores.Estrella(x, y)
			estrella.escala=[3,0,0.75],.1
			pilas.colisiones.agregar(estrella,torreta.habilidades.DispararConClick.proyectiles,asignar_arma_mejorada)
			pilas.tareas.agregar(3, eliminar_estrella, estrella)
			# Creacion de enemigos 
    if fin_de_juego:
        return False
    else:
        return True

#Determinamos el arma primaria de la torreta    
def asignar_arma_simple():
	# Asignar la munición sencilla
	torreta.municion=pilasengine.actores.Bala

#Le asgignamos a la torreta el nuevo proyectil    
def asignar_arma_mejorada(estrella, proyectil):
    global torreta
    torreta.municion=pilasengine.actores.Misil
    estrella.eliminar()
    pilas.tareas.agregar(10, asignar_arma_simple)
    pilas.avisar("NUEVA MEJORA ADQUIRIDA")
        
def eliminar_estrella(estrella):
	estrella.eliminar()

torreta = pilas.actores.Torreta(enemigos=monos, municion_bala_simple="bala", cuando_elimina_enemigo=mono_destruido)
torreta.aprender(pilas.habilidades.MoverseConElTeclado)
torreta.aprender(pilas.habilidades.LimitadoABordesDePantalla)
torreta.municion=pilasengine.actores.Bala
pilas.tareas.agregar(1, crear_mono)
pilas.colisiones.agregar(torreta, monos, game_over)
# Arrancar el juego
pilas.ejecutar()
