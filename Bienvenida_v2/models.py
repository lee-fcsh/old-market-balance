from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import datetime

author = 'Luis Andrade'

doc = """
App para mostrar el mensaje de bienvenida General para sesiones con múltiples apps.
"""


class Constants(BaseConstants):
    name_in_url = 'Bienvenida_v2'
    players_per_group = None
    num_rounds = 1
    anio_max = datetime.datetime.now().year * 100000 + 99999


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    matricula = models.StringField(label='Matrícula')

