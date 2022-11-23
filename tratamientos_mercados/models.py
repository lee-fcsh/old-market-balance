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
    name_in_url = 'tratamientos_mercados'
    players_per_group = None
    num_rounds = 10

    ganancias_template = 'tratamientos_mercados/Ganancias.html'
    ganancias_template2 = 'tratamientos_mercados/Ganancias_etapa1.html'

    tratamientos = [0, 1, 2, 3]

    valor_fijo_abogado = 2
    valor_porcentual_abogado = 0.10
    valor_d = 1.1


    # Valores de las cartas para el mercado
    cartas_compradores = [6, 8, 10]
    cartas_vendedores = [1, 3, 5]

    tipo_compradores = ['L', 'L', 'H']
    tipo_vendedores = ['H', 'H', 'L']


class Subsession(BaseSubsession):
    def creating_session(self):
        new_structure = [[], [], [], []]
        id = 0
        n_participants_n3 = int(self.session.config['participants_treatment_n3'])
        n_participants_n4 = int(self.session.config['participants_treatment_n4'])
        n_participants_n5 = int(self.session.config['participants_treatment_n5'])
        n_participants_n6 = int(self.session.config['participants_treatment_n6'])
        # fixme aqui debe ser cuantos mercados se van a formar
        jugadores = self.get_players()
        numero_participantes_tratamientos = [n_participants_n3, n_participants_n4, n_participants_n5, n_participants_n6]  #SUMA DE LA LISTA DEBE SER EL NUMERO DE PARTICIPANTES

        for p in range(1, len(jugadores)+1):
            while (len(new_structure[Constants.tratamientos[id]]) == numero_participantes_tratamientos[Constants.tratamientos[id]]):
                id+=1

            n_tratamiento = Constants.tratamientos[id]
            if len(new_structure[n_tratamiento]) < numero_participantes_tratamientos[n_tratamiento]:
                new_structure[n_tratamiento].append(p)

        self.set_group_matrix(new_structure)
        # print(self.get_group_matrix()) # will output this:
        letraC = 1   # IDENTIFICADOR DEL COMPRADOR
        letraV = 1   # IDENTIFICADOR DEL VENDEDOR
        for g in self.get_groups():
            g.id_in_subsession = g.id_in_subsession - 1
            for p in g.get_players():
                if p.role() == 'vendedor':
                    p.identificador = "V" + str(letraV)
                    letraV += 1
                    
                elif p.role() == 'comprador':
                    p.identificador = "C" + str(letraC)
                    letraC += 1


            for r in range(1,Constants.num_rounds + 1):
                numero_jugadores = len(g.get_players()) #Jugadores del mercado
                numero_vendedores = numero_jugadores // 2
                numero_compradores = numero_jugadores - numero_vendedores

                n_vendedores_H = numero_vendedores // 2
                n_vendedores_L = numero_vendedores - n_vendedores_H

                n_compradores_L = numero_compradores // 2
                n_compradores_H = numero_compradores - n_compradores_L

                if g.id_in_subsession == 1 or g.id_in_subsession == 3:
                    for p in g.get_players():
                        # ASIGNACION EXACTA DE H Y L
                        while True:
                            p.in_round(r).elegir_Carta()
                            if p.role() == 'vendedor':
                                if p.in_round(r).tipo_valor == 'H' and n_vendedores_H - 1 >= 0:
                                    n_vendedores_H-=1
                                    break
                                elif p.in_round(r).tipo_valor == 'L' and n_vendedores_L - 1 >= 0:
                                    n_vendedores_L-=1
                                    break
                                else:
                                    continue  
                            else:
                                if p.in_round(r).tipo_valor == 'H' and n_compradores_H - 1 >= 0:
                                    n_compradores_H-=1
                                    break
                                elif p.in_round(r).tipo_valor == 'L' and n_compradores_L - 1 >= 0:
                                    n_compradores_L-=1
                                    break
                                else:
                                    continue 
                else:
                    for p in g.get_players():
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
                    break



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

    aceptar_proceso = models.StringField(blank=True)       # Aceptar el procedimiento de compra o venta

    abogado = models.StringField(           #Para la contratacion de abogado
        choices=['Si', 'No'],
        doc="""Esto es la decision final del jugador""",
        widget=widgets.RadioSelect,
    )

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
