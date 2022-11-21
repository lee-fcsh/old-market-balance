from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Results(Page):
    def vars_for_template(self):
        dict_results = (self.participant.vars).get('dict_results', {})
        return {
            'opciones': dict_results,
            'total_pagar': self.participant.payoff_plus_participation_fee()
        }

page_sequence = [Results]
