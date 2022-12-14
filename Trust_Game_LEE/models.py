from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Cordova Balon Alex Alberto'

doc = """
Juego de Confianza de dos roles.
"""


class Constants(BaseConstants):
    name_in_url = 'Trust_Game_LEE'
    players_per_group = 2
    num_rounds = 2

    template_jugadores = 'Trust_Game_LEE/instrucciones_jugadores.html'

    dotacion_inicial_int =10
    factor_multiplicador = 2


class Subsession(BaseSubsession):
    def creating_session(self):
        for ply in self.in_round(self.round_number).get_players():
            if self.round_number == 1:
                if ply.id_in_group == 1:
                    ply.in_round(self.round_number).rol = "Donador"

                elif ply.id_in_group == 2:
                    ply.in_round(self.round_number).rol = "Recibidor"
            else:
                if ply.in_round(self.round_number-1).rol == "Donador":
                    ply.in_round(self.round_number).rol = "Recibidor"
                elif ply.in_round(self.round_number-1).rol == "Recibidor":
                    ply.in_round(self.round_number).rol = "Donador"

#### FIXMEE
class Group(BaseGroup):
    sent_amount = models.IntegerField(
        label="¿Cuánto desea enviar al participante B?",
        min = 0, max = Constants.dotacion_inicial_int,
        widget=widgets.RadioSelect,
        choices=range(0, Constants.dotacion_inicial_int + 1)
    )
    sent_back_amount = models.IntegerField(
        label="¿Cuánto desea devolver?",
        widget=widgets.RadioSelect,
        min=0
    )
    def sent_back_amount_max(self):
        return self.sent_amount * Constants.factor_multiplicador


class Player(BasePlayer):
    rol  = models.StringField()
    ganancias = models.IntegerField()
    
