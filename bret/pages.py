from __future__ import division

# from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    # only display instruction in round 1
    def is_displayed(self):
        return self.subsession.round_number == 1

    # variables for use in template
    def vars_for_template(self):
        if self.session.config.get('valor_de_caja') == None:
            valor_de_caja = Constants.box_value
        else:
            valor_de_caja = self.session.config.get('valor_de_caja')
        
        nombre_sesion = self.session.config.get('name')
        if nombre_sesion == 'corrupccion_terceros':
            titulo = 'Instrucciones'
        else:
            titulo = 'Tarea 1 - Instrucciones'

        return {
            'num_rows':             Constants.num_rows,
            'num_cols':             Constants.num_cols,
            'num_boxes':            Constants.num_rows * Constants.num_cols,
            'num_nobomb':           Constants.num_rows * Constants.num_cols - 1,
            'box_value':            Constants.box_value,
            'time_interval':        Constants.time_interval,
            'titulo': titulo,
        }


# ******************************************************************************************************************** #
# *** CLASS BOMB RISK ELICITATION TASK *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form fields on player level
    form_model = 'player'
    form_fields = [
        'bomb',
        'boxes_collected',
        'bomb_row',
        'bomb_col',
    ]

    # BRET settings for Javascript application
    def vars_for_template(self):
        reset = self.participant.vars.get('reset',False)
        if reset:
            del self.participant.vars['reset']

        input = not Constants.devils_game if not Constants.dynamic else False

        otree_vars = {
            'reset':            reset,
            'input':            input,
            'random':           Constants.random,
            'dynamic':          Constants.dynamic,
            'num_rows':         Constants.num_rows,
            'num_cols':         Constants.num_cols,
            'feedback':         Constants.feedback,
            'undoable':         Constants.undoable,
            'box_width':        Constants.box_width,
            'box_height':       Constants.box_height,
            'time_interval':    Constants.time_interval,
        }
        nombre_sesion = self.session.config.get('name')
        if nombre_sesion == 'corrupcion_terceros':
            titulo = 'Tarea 1 - '
        else:
            titulo = None

        return {
            'otree_vars':       otree_vars,
            'titulo': titulo
        }

    def before_next_page(self):
        self.participant.vars['reset'] = True
        self.player.set_payoff()


# ******************************************************************************************************************** #
# *** CLASS RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # only display results after all rounds have been played
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    # variables for use in template
    def vars_for_template(self):
        total_payoff = sum([p.payoff for p in self.player.in_all_rounds()])
        self.participant.vars['bret_payoff'] = total_payoff
        self.participant.vars["ronda_gan_bret"] = self.participant.vars["round_to_pay"]

        nombre_sesion = self.session.config.get('name')
        if nombre_sesion == 'corrupcion_terceros':
            titulo = 'Tarea 1 - Resultados Finales'
        else:
            titulo = 'Resultados'

        return {
            'player_in_all_rounds':   self.player.in_all_rounds(),
            'box_value':              Constants.box_value,
            'boxes_total':            Constants.num_rows * Constants.num_cols,
            'boxes_collected':        self.player.boxes_collected,
            'bomb':                   self.player.bomb,
            'bomb_row':               self.player.bomb_row,
            'bomb_col':               self.player.bomb_col,
            'round_result':           self.player.round_result,
            'round_to_pay':           self.participant.vars['round_to_pay'],
            'payoff':                 self.player.payoff,
            'total_payoff':           total_payoff,
            'titulo':                 titulo,
        }


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Decision]

if Constants.instructions:
    page_sequence.insert(0,Instructions)

if Constants.results:
    page_sequence.append(Results)
