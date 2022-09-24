#pylint: disable=import-error
"Module to create the app in Otree, Goodbye experiment"
from otree.api import (
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
)

AUTHOR ="tatiana Lisbeth Yepez Vera"

DOC = """
App para mostrar el mensaje de de despedida general para sesiones con múltiples apps.
"""
class Constants(BaseConstants):
    "constants for the GoodBye"
    name_in_url = 'Goodbye'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    "Classes needed for the experiment"

class Group(BaseGroup):
    "Classes needed for the experiment"


class Player(BasePlayer):
    "Classes needed for the experiment"
