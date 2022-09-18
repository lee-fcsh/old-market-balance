from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import datetime

author = 'Luis Andrade'

doc = """
App para mostrar el mensaje de bienvenida General para sesiones con múltiples apps.
"""
# funcion para generar diccionario de ips, las claves son indices del 194 al 228,
# los valores, números del 1 al 35 respectivamente


class Constants(BaseConstants):
    name_in_url = 'Bienvenida_v2'
    players_per_group = None
    num_rounds = 1
    anio_max = datetime.datetime.now().year * 100000 + 99999


class Subsession(BaseSubsession):

    def creating_session(self):
        # se guarda el diccionario de ip's como variable de sesión
        print('nombre de sesion: ', self.session.config['name'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    matricula = models.PositiveIntegerField(min=199000000, max=Constants.anio_max)

