from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Instrucciones_Seccion1(Page):
    def is_displayed(self):
        return self.player.round_number % 2 == 1

class Instrucciones_Seccion2(Page):
    def is_displayed(self):
        return self.player.round_number % 2 == 0

class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']
    def is_displayed(self):
        return self.player.rol == "Donador"
    def vars_for_template(self):
        return dict(
            dotacion_inicial_int = Constants.dotacion_inicial_int
        )

class WaitForDonador(WaitPage):
    def after_all_players_arrive(self):
        pass

class Send_Back(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']
    def is_displayed(self):
        return self.player.rol == "Recibidor"

    def vars_for_template(self):
        return dict(
            tripled_amount = self.group.sent_amount * Constants.factor_multiplicador
        )

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        jugadores = self.group.get_players()
        for p in jugadores:
            rol = p.rol
            if rol == "Donador":
                p.ganancias = Constants.dotacion_inicial - self.group.sent_amount + self.group.sent_back_amount
            else:
                p.ganancias = (self.group.sent_amount * Constants.factor_multiplicador) - self.group.sent_back_amount

class Results(Page):
    def vars_for_template(self):
        return dict(
            tripled_amount = self.group.sent_amount * Constants.factor_multiplicador
        )
    


page_sequence = [Instrucciones_Seccion1,Instrucciones_Seccion2,Send, WaitForDonador, Send_Back, ResultsWaitPage, Results]
