#pylint: disable=import-error
"Module to create the app in Otree"
from otree.api import Page



class Inicio(Page):
    'Class Inicio'
    def is_displayed(self):
        'Function displayed'
        return self.player.round_number == 1


page_sequence = [Inicio]
