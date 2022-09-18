from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import random

class Introduction(Page):

    def before_next_page(self):
        self.player.calcularNumMaquina()
        self.participant.vars['maquina'] = self.player.maquina
        print ('maquina: ', self.player.maquina)


class Decision(Page):
    form_model = models.Player
    form_fields = ['dec_{}'.format(i) for i in range(1, 16)]
    
    def vars_for_template(self):

        opciones = ['A','I', 'B']
        # indices
        indices = [i for i in range(1, 16)]

        return {
            'opciones': opciones,
            'mult': zip(indices, Constants.valores_de_A, Constants.valores_de_B)
        }

    
class WPF(WaitPage):
    
    def after_all_players_arrive(self):
        self.group.calcular_ganancias()

class Results(Page):
    def vars_for_template(self):
        maquina = 0
        op = ''
        pago = 0
        plazo = ''
        for p in self.subsession.get_players():
            if (p.ganador):
                maquina = p.maquina
                op = p.dec_gan
                pago = p.pago
                plazo = p.plazo
        
        return {
            'maquina' : maquina,
            'op' : op,
            'pago' : pago,
            'plazo' : plazo
        }



page_sequence = [
    Introduction,
    Decision,
    WPF,
    Results
]
