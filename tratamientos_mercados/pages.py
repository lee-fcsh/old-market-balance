from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
import string
from .models import Constants
from . import models
import operator
import random as rd

#################### PAGINAS DE INTRUCCIONES PARA EL EXPERIMENTO DE MERCADO   ###############################

class Introduccion0(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        if self.group.id_in_subsession == 1 or self.group.id_in_subsession == 3:
            texto1 = 'Asimismo, mantendrá el mismo valor (costo de producción o presupuesto) en cada ronda.'
        else:
            texto1 = 'Sin embargo, usted enfrentará un valor (costo de producción o presupuesto) distinto en cada ronda de negociación.'

        if self.group.id_in_subsession == 1 or self.group.id_in_subsession == 2:
            texto2 = 'El COSTO de contratar un mediador es $ c.'
            texto3 = '$ c'
        else:
            texto2 = f'El COSTO (c) de contratar un mediador es un porcentaje fijo ({Constants.valor_porcentual_abogado * 100}%) del valor asignado a cada participante.'
            texto3 = f' c=  {Constants.valor_porcentual_abogado*100}% del valor asignado'

        return{
            'texto1' : texto1,
            'texto2' : texto2,
            'texto3' : texto3,
        }

class Ganancia_ronda0(Page):
    def is_displayed(self):
        return self.round_number == 1

##############################################################################################

class Carta_Precio(Page):
    def is_displayed(self):
        return self.player.role() == 'vendedor' and self.round_number == 1
    timeout_seconds = 60
    timer_text = 'Tiempo limite:'
    
    def vars_for_template(self):
        return {
            'ronda' : self.round_number,
            }

class Carta_Oferta(Page):
    def is_displayed(self):
        return self.player.role() == 'comprador' and self.round_number == 1
    timeout_seconds = 60
    timer_text = 'Tiempo limite:'

    def vars_for_template(self):
        return {
            'ronda' : self.round_number,
            }

class Prev_negociacion(WaitPage):
    pass

class Auction(Page):
    timeout_seconds = 180
    def vars_for_template(self):
        compradores = []
        vendedores = []
        valores_vendidos = []
        id_vendidos = []
        actualp = 999999999999999999999999999
        actualo = 0

        for p in self.group.get_players():
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
            'ronda' : self.round_number,
            'id' : self.player.identificador,
            'precio_actual' : actualp,
            'oferta_actual' : actualo,
            'ultimo_precio' : ultimo_precio,
            'ultima_oferta' : ultima_oferta,
            'valores_vendidos': valores_vendidos,

        }

class Abogado(Page):
    def is_displayed(self):
        if self.group.id_in_subsession == 1 or self.group.id_in_subsession == 2:
            self.player.abogado = 'No'
        return self.player.valor_venta != None and (self.group.id_in_subsession == 3 or self.group.id_in_subsession == 4)

    form_model = 'player'
    form_fields = ['abogado']

    def vars_for_template(self):
        if self.group.id_in_subsession == 1 or self.group.id_in_subsession == 2:
                costo_abogado = Constants.valor_fijo_abogado
        else:
            costo_abogado = Constants.valor_porcentual_abogado * self.player.carta
        agente_contraparte = ''
        for p2 in self.group.get_players():    # BUSCAMOS CON  QUIEN HIZO MATCH
            if self.player.id_venta == p2.id_venta and self.player.identificador != p2.identificador and p2.id_venta!= None:  # BUSCAMOS SU MATCH
                agente_contraparte = p2.tipo_valor
        return{
            'costo_abogado' : costo_abogado,
            'agente_contraparte' : agente_contraparte
        }

class Renegar(Page):
    def is_displayed(self):
        return self.player.valor_venta != None

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
    
    def before_next_page(self):
        if self.player.abogado == 'Si':
            self.player.aceptar_proceso = 'Aceptar'
        if self.player.aceptar_proceso is None:
            self.player.aceptar_proceso = 'Renegar'

    def error_message(self, values):
        if self.player.abogado != 'Si' and values['aceptar_proceso'] == None:
            return 'Seleccione una opcion en la decisión'


## Pagina para hacer calculos antes de mostrar resultados
class RenegarWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p1 in self.group.get_players():    # RECORREMOS TODOS LOS JUGADORES PARA ANALIZAR
            if self.group.id_in_subsession == 1 or self.group.id_in_subsession == 2:
                costo_abogado = Constants.valor_fijo_abogado
            else:
                costo_abogado = Constants.valor_porcentual_abogado * p1.carta

            if p1.valor_venta != None:              # VERIFICAMOS QUE HAYAN HECHO MATCH
                ################### SI EL JUGADOR ES VENDEDOR   ##########################
                if p1.role() == 'vendedor':         
                    for p2 in self.group.get_players():    # BUSCAMOS CON  QUIEN HIZO MATCH
                        if p1.id_venta == p2.id_venta and p1.identificador != p2.identificador:  # BUSCAMOS SU MATCH
                            """ 
                            La ganancia acontinuacion, probablemente su forma de calcular se repite en codigo, por lo que este se podria reducir,
                            sin embargo, se dejo de esta forma por si se necesita cambiar el valor de ganancia de un caso especifico.
                            """
                            if p1.aceptar_proceso == 'Renegar': # RENEGO
                                if p2.aceptar_proceso == 'Renegar':                             # P2 RENEGO
                                    p1.ganancia = 0
                                elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'No':    # P2 ACEPTO Y NO TIENE ABOGADO
                                    p1.ganancia = p1.valor_venta
                                elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'Si':    # P2 ACEPTO Y TIENE ABOGADO
                                    p1.ganancia = p1.valor_venta - p1.carta - Constants.valor_d*costo_abogado

                            else:   # NO RENEGO
                                if p1.abogado == 'No':   # P1 NO ACEPTO ABOGADO
                                    if p2.aceptar_proceso == 'Renegar':                             # P2 RENEGO
                                        p1.ganancia = - p1.carta
                                    elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'No':    # P2 ACEPTO Y NO TIENE ABOGADO
                                        p1.ganancia = p1.valor_venta - p1.carta
                                    elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'Si':    # P2 ACEPTO Y TIENE ABOGADO
                                        p1.ganancia = p1.valor_venta - p1.carta

                                else:           # P1 ACEPTO ABOGADO
                                    if p2.aceptar_proceso == 'Renegar':                             # P2 RENEGO
                                        p1.ganancia = p1.valor_venta - p1.carta - costo_abogado
                                    elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'No':    # P2 ACEPTO Y NO TIENE ABOGADO
                                        p1.ganancia = p1.valor_venta - p1.carta - costo_abogado
                                    elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'Si':    # P2 ACEPTO Y TIENE ABOGADO
                                        p1.ganancia = p1.valor_venta - p1.carta - costo_abogado



                ################### SI EL JUGADOR ES COMPRADOR   ##########################
                elif p1.role() == 'comprador':
                    for p2 in self.group.get_players():    # BUSCAMOS CON  QUIEN HIZO MATCH
                        if p1.id_venta == p2.id_venta and p1.identificador != p2.identificador:  # BUSCAMOS SU MACH
                            """ 
                            La ganancia acontinuacion, probablemente su forma de calcular se repite en codigo, por lo que este se podria reducir,
                            sin embargo, se dejo de esta forma por si se necesita cambiar el valor de ganancia de un caso especifico.
                            """
                            if p1.aceptar_proceso == 'Renegar': # RENEGO
                                if p2.aceptar_proceso == 'Renegar':                             # P2 RENEGO
                                    p1.ganancia = 0
                                elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'No':    # P2 ACEPTO Y NO TIENE ABOGADO
                                    p1.ganancia = p1.carta
                                elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'Si':    # P2 ACEPTO Y TIENE ABOGADO
                                    p1.ganancia = p1.carta - p1.valor_venta - Constants.valor_d*costo_abogado

                            else:   # NO RENEGO
                                if p1.abogado == 'No':   # P1 NO ACEPTO ABOGADO
                                    if p2.aceptar_proceso == 'Renegar':                             # P2 RENEGO
                                        p1.ganancia = p1.valor_venta*-1
                                    elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'No':    # P2 ACEPTO Y NO TIENE ABOGADO
                                        p1.ganancia = p1.carta - p1.valor_venta
                                    elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'Si':    # P2 ACEPTO Y TIENE ABOGADO
                                        p1.ganancia = p1.carta - p1.valor_venta

                                else:           # P1 ACEPTO ABOGADO
                                    if p2.aceptar_proceso == 'Renegar':                             # P2 RENEGO
                                        p1.ganancia = p1.carta - p1.valor_venta - costo_abogado
                                    elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'No':    # P2 ACEPTO Y NO TIENE ABOGADO
                                        p1.ganancia = p1.carta - p1.valor_venta - costo_abogado
                                    elif p2.aceptar_proceso == 'Aceptar' and p2.abogado == 'Si':    # P2 ACEPTO Y TIENE ABOGADO
                                        p1.ganancia = p1.carta - p1.valor_venta - costo_abogado  
            else:
                p1.valor_venta = 0
                p1.ganancia = 0
                p1.aceptar_proceso = ""
                p1.abogado = ""
                      

class Results(Page):
    def vars_for_template(self):
        if self.player.aceptar_proceso == 'Renegar':
            renegar = 'SI'
        elif self.player.aceptar_proceso == "":
            renegar = ''
        else:
            renegar = 'NO'
        
        mediador_contraparte = ''
        renegar_contraparte = ''
        agente_contraparte = ''
        for p2 in self.group.get_players():    # BUSCAMOS CON  QUIEN HIZO MATCH
            if self.player.id_venta == p2.id_venta and self.player.identificador != p2.identificador and p2.id_venta!= None:  # BUSCAMOS SU MATCH
                agente_contraparte = p2.tipo_valor
                mediador_contraparte = p2.abogado
                if p2.abogado == None:
                    mediador_contraparte = 'No'
                if p2.aceptar_proceso == 'Renegar':
                    renegar_contraparte = 'SI'
                else:
                    renegar_contraparte = 'NO'
        
        return{
            'ronda' : self.round_number,
            'ganancia' : self.player.ganancia,
            'renegar' : renegar,
            'mediador': self.player.abogado,
            'mediador_contraparte': mediador_contraparte,
            'agente_contraparte' : agente_contraparte,
            'renegar_contraparte' : renegar_contraparte
        }

    def before_next_page(self):
        self.participant.vars['ronda_aleatoria'] = rd.randint(1, Constants.num_rounds)


class Resultados_Finales(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    def vars_for_template(self):
        ronda_aleatoria = self.participant.vars['ronda_aleatoria']
        ganancia_total = self.player.in_round(ronda_aleatoria).ganancia
        self.player.payoff = ganancia_total * 1.5

        ########### CALCULO DE PAYOFF A PARTICIPANTE POR CADA APP #####################################
        self.participant.vars['dict_results'] = (self.participant.vars).get('dict_results', {})
        self.participant.vars['dict_results']['market_etapa2'] =dict(
            label='Etapa 2',
            payoff=0
        )
        for round in range(1, Constants.num_rounds+1):
            self.participant.vars['dict_results']['market_etapa2']['payoff'] += self.player.in_round(round).payoff
        #################################################################################################

        return{
            'ganancia_total' : ganancia_total,
            'ronda_seleccionada':ronda_aleatoria
        }

page_sequence = [
    Introduccion0,
    Ganancia_ronda0,
    Carta_Precio,
    Carta_Oferta,
    Prev_negociacion,
    Auction,
    Abogado,
    Renegar,
    RenegarWaitPage,
    Results,
    Resultados_Finales,
]
