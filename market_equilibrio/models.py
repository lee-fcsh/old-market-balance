from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint
from django import forms

author = 'Cordova Balon Alex Alberto'

doc = """
Prueba del tiempo real de el mercado
"""


class Constants(BaseConstants):
    name_in_url = 'market_equilibrio'
    players_per_group = 6
    num_rounds = 6 

    # Valores de las cartas para el mercado
    cartas_compradores = [6, 8, 10]
    cartas_vendedores = [1, 3, 5]

    tipo_compradores = ['L', 'L', 'H']
    tipo_vendedores = ['H', 'H', 'L']


class Subsession(BaseSubsession):
    def creating_session(self):
        letraC = 1   # IDENTIFICADOR DEL COMPRADOR
        letraV = 1   # IDENTIFICADOR DEL VENDEDOR
        for g in self.get_groups():
            numero_jugadores = len(g.get_players()) #Jugadores del mercado
            numero_vendedores = numero_jugadores // 2
            numero_compradores = numero_jugadores - numero_vendedores

            n_vendedores_H = numero_vendedores // 2
            n_vendedores_L = numero_vendedores - n_vendedores_H

            n_compradores_L = numero_compradores // 2
            n_compradores_H = numero_compradores - n_compradores_L
            

            for p in g.get_players():
                if p.role() == 'vendedor':
                    p.identificador = "V" + str(letraV)
                    letraV += 1
                    
                elif p.role() == 'comprador':
                    p.identificador = "C" + str(letraC)
                    letraC += 1

                # ASIGNACION EXACTA DE H Y L
                while True:
                    p.elegir_Carta()
                    if p.role() == 'vendedor':
                        if p.tipo_valor == 'H' and n_vendedores_H - 1 >= 0:
                            n_vendedores_H-=1
                            break
                        elif p.tipo_valor == 'L' and n_vendedores_L - 1 >= 0:
                            n_vendedores_L-=1
                            break
                        else:
                          continue  
                    else:
                        if p.tipo_valor == 'H' and n_compradores_H - 1 >= 0:
                            n_compradores_H-=1
                            break
                        elif p.tipo_valor == 'L' and n_compradores_L - 1 >= 0:
                            n_compradores_L-=1
                            break
                        else:
                          continue 

                for ronda in p.in_all_rounds():
                    ronda.carta = p.in_all_rounds()[0].carta
                    ronda.tipo_valor = p.in_all_rounds()[0].tipo_valor


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # DEFINICION DEL ROL DEL JUGADOR 
    def role(self):
        if self.id_in_group % 2 == 1:
            return 'vendedor'
        if self.id_in_group % 2 == 0:
            return 'comprador'
    
    identificador = models.StringField()    # Identificacion de Letra
    carta = models.IntegerField()   #Carta del numero
    precio = models.FloatField()    #Precio que propone el jugador -> Solo para vendedores
    oferta = models.FloatField()    #Precio que oferta el jugador para la compra -> Solo para vendedores
    tipo_valor = models.StringField()   # El tipo de valor si es H o L
    
    valor_venta = models.FloatField() # Valor con el que se concreto la venta
    id_venta = models.StringField() #Id de la venta realizada, para formar el grupo

    ganancia = models.FloatField()  # Ganancia de cada ronda

    aceptar_proceso = models.StringField()       # Aceptar el procedimiento de compra o venta


    ##########################  CARTA Y PRECIO   ################################
    def elegir_Carta(self):
        i_num_v = randint(0, len(Constants.cartas_vendedores) - 1)
        i_num_c = randint(0, len(Constants.cartas_compradores) - 1)
        num_v = Constants.cartas_vendedores[i_num_v]
        num_c = Constants.cartas_compradores[i_num_c]

        if self.role() == 'comprador':
            self.carta = num_c
            self.tipo_valor = Constants.tipo_compradores[i_num_c]

        elif self.role() == 'vendedor':
            self.carta = num_v
            self.tipo_valor = Constants.tipo_vendedores[i_num_v]

    ######################### CUESTIONARIO #####################################
    pregunta1 = models.StringField()
    pregunta2 = models.StringField()
    pregunta3 = models.StringField()
    pregunta4 = models.StringField()
