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


author = 'Alex Alberto Cordova Balon'

doc = """
Tabla de resultados de todas las sessiones realizadas con el total de pago mostrado en pantalla.
"""


class Constants(BaseConstants):
    name_in_url = 'results_matrix'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
