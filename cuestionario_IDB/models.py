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
Cuestionario de Confianza - 2019 IDB/LAPOP 
"""


class Constants(BaseConstants):
    name_in_url = 'cuestionario_IDB'
    players_per_group = None
    num_rounds = 1
    text_consentimiento = 'cuestionario_IDB/text_consentimiento.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # CONSENTIMIENTO PARA REALIZAR LA ENCUESTA
    offer_accepted = models.BooleanField()

    # PARTE 1 DEL QUIZZ
    CI1 = models.IntegerField(blank=True)
    CI2 = models.IntegerField(blank=True)
    CI3 = models.IntegerField(blank=True)
    CI4 = models.IntegerField(blank=True)
    CI5 = models.IntegerField(blank=True)
    CI6 = models.IntegerField(blank=True)
    CI7 = models.IntegerField(blank=True)
    CI8 = models.IntegerField(blank=True)
    CI9 = models.IntegerField(blank=True)
    CI10 = models.IntegerField(blank=True)
    CI11 = models.IntegerField(blank=True)
    CI12 = models.IntegerField(blank=True)
    CI13 = models.IntegerField(blank=True)
    CI14 = models.IntegerField(blank=True)
    CI15 = models.IntegerField(blank=True)
    CI16 = models.IntegerField(blank=True)
    CI17 = models.IntegerField(blank=True)

    CI18 = models.StringField(blank=True)
    CI19 = models.StringField(blank=True)
    CI20 = models.StringField(blank=True)


    # PARTE 2 DEL QUIZZ
    CP1 = models.IntegerField(blank=True)
    CP2 = models.IntegerField(blank=True)
    CP3 = models.IntegerField(blank=True)
    CP4 = models.IntegerField(blank=True)
    CP5 = models.IntegerField(blank=True)

    # PARTE 3 DEL QUIZZ
    CG1 = models.IntegerField(blank=True)
    CG2 = models.IntegerField(blank=True)
    CG3 = models.IntegerField(blank=True)
    CG4 = models.IntegerField(blank=True)
    CG5 = models.IntegerField(blank=True)
    CG6 = models.IntegerField(blank=True)
    CG7 = models.IntegerField(blank=True)
    CG8 = models.IntegerField(blank=True)
    CG9 = models.IntegerField(blank=True)
    CG10 = models.IntegerField(blank=True)
    CG11 = models.IntegerField(blank=True)
    CG12 = models.IntegerField(blank=True)
    CG13 = models.IntegerField(blank=True)
    CG14 = models.IntegerField(blank=True)
    CG15 = models.IntegerField(blank=True)
    CG16 = models.IntegerField(blank=True)
    CG17 = models.IntegerField(blank=True)
    CG18 = models.IntegerField(blank=True)
    CG19 = models.IntegerField(blank=True)
    CG20 = models.IntegerField(blank=True)

    # PARTE 4 DEL QUIZZ
    JD1 = models.StringField(blank=True)
    JD2 = models.StringField(blank=True)
    JD3 = models.StringField(blank=True)
    JD4 = models.StringField(blank=True)

    JD5 = models.IntegerField(blank=True)
    JD6 = models.IntegerField(blank=True)
    JD7 = models.IntegerField(blank=True)
    JD8 = models.IntegerField(blank=True)

    # PARTE 5 DEL QUIZZ
    PS1 = models.StringField(blank=True)
    PS2 = models.IntegerField(blank=True, min=10)
    PS3 = models.StringField(blank=True)
    PS4 = models.IntegerField(blank=True)
    PS5 = models.StringField(blank=True)
    PS6 = models.StringField(blank=True)
    PS6P = models.StringField(blank=True)
    PS7 = models.StringField(blank=True)
    PS8 = models.StringField(blank=True)

