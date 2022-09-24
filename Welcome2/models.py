#pylint: disable=import-error
'Import module for welcome'
from otree.api import (
    BaseConstants, BaseSubsession, BaseGroup, BasePlayer,)

AUTHOR = 'Tatiana Yepez'
DOC = """
Pagina de bienvenida en general
"""


class Constants(BaseConstants):
    'Class content constants'
    name_in_url = 'Welcome2'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    'Class necesary'


class Group(BaseGroup):
    "This class contains the participants of the game with your total of contributions"


class Player(BasePlayer):
    "This class is for the players"
