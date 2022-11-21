from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
import string
from .models import Constants
from . import models
import operator
import random as rd

#################### PAGINAS DE INTRUCCIONES PARA EL EXPERIMENTO DE MERCADO   ###############################

class Introduccion(Page):
    def is_displayed(self):
        return self.round_number == 1

class Entrenamiento_part1(Page):
    def is_displayed(self):
        return self.round_number == 1

class Entrenamiento_part2(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instrucciones_Negociacion_part1(Page):
    def is_displayed(self):
        return self.round_number == 4

class Instrucciones_Negociacion_part2(Page):
    def is_displayed(self):
        return self.round_number == 4

##############################################################################################

class Carta_Precio(Page):
    def is_displayed(self):
        return self.player.role() == 'vendedor' and self.round_number == 1
    timeout_seconds = 60
    
    def vars_for_template(self):
        ronda_presente = self.round_number
        if ronda_presente > 3:
            ronda_presente = ronda_presente - 3
        ronda_total = Constants.num_rounds // 2
        return {
            'ronda' : ronda_presente,
            'ronda_total': ronda_total
            }

class Carta_Oferta(Page):
    def is_displayed(self):
        return self.player.role() == 'comprador' and self.round_number == 1
    timeout_seconds = 60

    def vars_for_template(self):
        ronda_presente = self.round_number
        if ronda_presente > 3:
            ronda_presente = ronda_presente - 3
        ronda_total = Constants.num_rounds // 2
        return {
            'ronda' : ronda_presente,
            'ronda_total': ronda_total
            }

class Prev_negociacion(WaitPage):
    pass

class Auction(Page):
    timeout_seconds = 300
    def vars_for_template(self):
        ronda_presente = self.round_number
        if ronda_presente > 3:
            ronda_presente = ronda_presente - 3
        ronda_total = Constants.num_rounds // 2

        compradores = []
        vendedores = []
        valores_vendidos = []
        id_vendidos = []
        actualp = 999999999999999999999999999
        actualo = 0

        for p in self.subsession.get_players():
            if p.valor_venta == None:
                if p.role() == 'comprador':
                    if p.oferta != None:
                        compradores.append({'name':p.identificador, 'value':p.oferta})
                    if p.oferta != None and p.oferta > actualo:
                        actualo = p.oferta
                    
                elif p.role() == 'vendedor':
                    if p.precio != None:
                        vendedores.append({'name':p.identificador, 'value':p.precio})
                    if p.precio != None and p.precio < actualp:
                        actualp = p.precio
            elif p.id_venta not in id_vendidos:
                valores_vendidos.append(p.valor_venta)
                id_vendidos.append(p.id_venta)
        ultimo_precio = self.player.precio
        ultima_oferta = self.player.oferta
        return {
            'objcompradores' : compradores,
            'objvendedores' : vendedores,
            'ronda' : ronda_presente,
            'ronda_total': ronda_total,
            'id' : self.player.identificador,
            'precio_actual' : actualp,
            'oferta_actual' : actualo,
            'ultimo_precio' : ultimo_precio,
            'ultima_oferta' : ultima_oferta,
            'valores_vendidos': valores_vendidos,

        }

class Renegar(Page):
    def is_displayed(self):
        return self.round_number > 3 and self.player.valor_venta != None

    form_model = 'player'
    form_fields = ['aceptar_proceso']

    def vars_for_template(self):
        agente_contraparte = ''
        for p2 in self.group.get_players():    # BUSCAMOS CON  QUIEN HIZO MATCH
            if self.player.id_venta == p2.id_venta and self.player.identificador != p2.identificador and p2.id_venta!= None:  # BUSCAMOS SU MATCH
                agente_contraparte = p2.tipo_valor
        return{
            'agente_contraparte' : agente_contraparte,
        }



## Pagina para hacer calculos antes de mostrar resultados
class RenegarWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p1 in self.group.get_players():    # RECORREMOS TODOS LOS JUGADORES PARA ANALIZAR
            if p1.valor_venta != None:              # VERIFICAMOS QUE HAYAN HECHO MATCH
                ################### SI EL JUGADOR ES VENDEDOR   ##########################
                if p1.role() == 'vendedor':         
                    for p2 in self.group.get_players():    # BUSCAMOS CON  QUIEN HIZO MATCH
                        if p1.id_venta == p2.id_venta and p1.identificador != p2.identificador:  # BUSCAMOS SU MATCH
                            """
                            La ganancia acontinuacion, probablemente su forma de calcular se repite en codigo, por lo que este se podria reducir,
                            sin embargo, se dejo de esta forma por si se necesita cambiar el valor de ganancia de un caso especifico.
                            """
                            if self.round_number > 3:
                                if p1.aceptar_proceso == 'Renegar': # RENEGO
                                    if p2.aceptar_proceso == 'Renegar':       # P2 RENEGO
                                        p1.ganancia = 0
                                    elif p2.aceptar_proceso == 'Aceptar':    # P2 ACEPTO
                                        p1.ganancia = p1.valor_venta

                                else:   # NO RENEGO
                                    if p2.aceptar_proceso == 'Renegar':      # P2 RENEGO
                                        p1.ganancia = - p1.carta
                                    elif p2.aceptar_proceso == 'Aceptar':    # P2 ACEPTO
                                        p1.ganancia = p1.valor_venta - p1.carta
                            else:
                                p1.ganancia = p1.valor_venta - p1.carta


                ################### SI EL JUGADOR ES COMPRADOR   ##########################
                elif p1.role() == 'comprador':
                    for p2 in self.group.get_players():    # BUSCAMOS CON  QUIEN HIZO MATCH
                        if p1.id_venta == p2.id_venta and p1.identificador != p2.identificador:  # BUSCAMOS SU MACH
                            """ 
                            La ganancia acontinuacion, probablemente su forma de calcular se repite en codigo, por lo que este se podria reducir,
                            sin embargo, se dejo de esta forma por si se necesita cambiar el valor de ganancia de un caso especifico.
                            """
                            if self.round_number > 3:
                                if p1.aceptar_proceso == 'Renegar': # RENEGO
                                    if p2.aceptar_proceso == 'Renegar':       # P2 RENEGO
                                        p1.ganancia = 0
                                    elif p2.aceptar_proceso == 'Aceptar':    # P2 ACEPTO 
                                        p1.ganancia = p1.carta

                                else:   # NO RENEGO
                                    if p2.aceptar_proceso == 'Renegar':      # P2 RENEGO
                                        p1.ganancia = p1.valor_venta*-1
                                    elif p2.aceptar_proceso == 'Aceptar':    # P2 ACEPTO
                                        p1.ganancia = p1.carta - p1.valor_venta
                            else:
                                p1.ganancia = p1.carta - p1.valor_venta   
            else:
                p1.valor_venta = 0
                p1.ganancia = 0
                p1.aceptar_proceso = ""


class Results(Page):
    def vars_for_template(self):
        if self.player.aceptar_proceso == 'Renegar':
            renegar = 'SI'
        elif self.player.aceptar_proceso == "":
            renegar = ''
        else:
            renegar = 'NO'
        renegar_contraparte = ''
        agente_contraparte = ''
        for p2 in self.group.get_players():    # BUSCAMOS CON  QUIEN HIZO MATCH
            if self.player.id_venta == p2.id_venta and self.player.identificador != p2.identificador and p2.id_venta!= None:  # BUSCAMOS SU MATCH
                agente_contraparte = p2.tipo_valor
                if p2.aceptar_proceso == 'Renegar':
                    renegar_contraparte = 'SI'
                else:
                    renegar_contraparte = 'NO'

        return{
            'ronda' : self.round_number,
            'ganancia' : self.player.ganancia,
            'renegar' : renegar,
            'agente_contraparte' : agente_contraparte,
            'renegar_contraparte' : renegar_contraparte
        }

    def before_next_page(self):
        self.participant.vars['ronda_ale_1'] = rd.randint(1, 3)
        self.participant.vars['ronda_ale_2'] = rd.randint(4, Constants.num_rounds)

class Resultados_Finales(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        ronda_aleatoria1 = self.participant.vars['ronda_ale_1']
        ronda_aleatoria2 = self.participant.vars['ronda_ale_2']
        ganancia_total_seccion1 = self.player.in_round(ronda_aleatoria1).ganancia
        ganancia_total_seccion2 = self.player.in_round(ronda_aleatoria2).ganancia

        return{
            'ganancia_total_seccion1' : ganancia_total_seccion1,
            'ronda_aleatoria1' : ronda_aleatoria1,
            'ganancia_total_seccion2' : ganancia_total_seccion2,
            'ronda_aleatoria2' : ronda_aleatoria2 - 3,
            'ganancia_total' : ganancia_total_seccion1 + ganancia_total_seccion2,
        }

class Cuestionario(Page):
    form_model = 'player'
    form_fields = ['pregunta1', 'pregunta2', 'pregunta3', 'pregunta4']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    def error_message(self, values):
        if values['pregunta1'] != "Comprador 1 y Vendedor 3":
            return 'Pregunta 1: Respuesta Incorrecta'

        elif values['pregunta2'] != "No se realiza la transacción, ambos ganan 0 y se pasa a la siguiente ronda.":
            return 'Pregunta 2: Respuesta Incorrecta'

        elif values['pregunta3'] != "Comprador 7 y Vendedor -5":
            return 'Pregunta 3: Respuesta Incorrecta'

        elif values['pregunta4'] != "Comprador -8 y Vendedor 8":
            return 'Pregunta 4: Respuesta Incorrecta'

class Fin_Etapa(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    Introduccion,
    Entrenamiento_part1,
    Entrenamiento_part2,
    Instrucciones_Negociacion_part1,
    Instrucciones_Negociacion_part2,
    Carta_Precio,
    Carta_Oferta,
    Prev_negociacion,
    Auction,
    Renegar,
    RenegarWaitPage,
    Results,
    Resultados_Finales,
    Cuestionario,
    Fin_Etapa,
]
