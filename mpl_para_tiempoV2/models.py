from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Washington Vélez'

doc = """
Your app description
"""

def generar_Dicc_Ip():
    dicc_ip = {}
    indice = 194
    for i in range(1, 36):
        dicc_ip[indice] = i
        indice += 1
    
    return dicc_ip

class Constants(BaseConstants):
    name_in_url = 'mpl_para_tiempoV2'
    players_per_group = None
    num_rounds = 1
    intructions_template = 'mpl_para_tiempoV2/Instrucciones.html'

    valores_de_A = [85.00, 85.00, 85.00, 85.00, 85.00, 85.00, 85.00, 85.00, 85.00, 85.00, 85.00, 85.00, 85.00, 85.00, 85.00]
    valores_de_B = [86.00, 86.00, 87.60, 88.40, 89.20, 90.00, 90.80, 91.60, 92.40, 93.20, 105.50, 110.30, 115.50, 123.40, 127.25]


class Subsession(BaseSubsession):
    def creating_session(self):
        # se guarda el diccionario de ip's como variable de sesión
        self.session.vars['dicc_ip'] = generar_Dicc_Ip()


class Group(BaseGroup):
    
    def calcular_ganancias(self):

        print('calcular ganador...')

        #se sortea a un ganador
        id_player = random.randint(1, self.session.num_participants)

        for p in self.get_players():
            if p.id_in_group == id_player:
                print ("Jugador ganador: ", p.id_in_group)
                p.ganador = True
                p.dec_gan = str(random.randint(1,15))
                p.participant.vars["dec_sorteada_mpl_tiempo"] = p.dec_gan
                print ("Decisión ganadora aleatoria: ", p.dec_gan)
                
                decision = 'dec_{}'.format(p.dec_gan)
                p.op_seleccionada = p.__getattribute__(decision)
                p.participant.vars["op_seleccionada_mpl_tiempo"] = p.op_seleccionada
                op_seleccionada = p.op_seleccionada

                if op_seleccionada =='I':
                    # se reescribe la variable con la opcion aleatoria (A o B)
                    p.op_seleccionada_ale = p.sortear_eleccion()
                    print ("Opción sorteada aleatoria:", p.op_seleccionada_ale)
                    p.participant.vars["op_seleccionada_ale_mpl_tiempo"] = p.op_seleccionada_ale
                    op_seleccionada = p.op_seleccionada_ale

                if op_seleccionada == 'A':
                    p.pago = Constants.valores_de_A[int(p.dec_gan)]
                    p.plazo = "7 días a partir de hoy"
                else:
                    p.pago = Constants.valores_de_B[int(p.dec_gan)]
                    p.plazo = "2 meses + 7 días a partir de hoy"

                p.participant.vars["pago_mpl_tiempo"] = p.pago
                p.participant.vars["plazo_mpl_tiempo"] = p.plazo
                print ("Ha ganado: ", p.pago)
                print ("Plazo: ", p.plazo)
            else:
                p.participant.vars["pago_mpl_tiempo"] = 0
                p.participant.vars["plazo_mpl_tiempo"] = ''





class Player(BasePlayer):

    #variable que se pone true si el participante gana en el sorteo
    ganador = models.BooleanField(initial=False)

    OPCIONES = (('A', ' '),('I', ' '),('B', ' '))
    
    dec_1 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_2 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_3 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_4 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_5 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_6 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_7 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_8 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_9 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_10 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_11 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_12 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_13 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_14 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())
    dec_15 = models.StringField(choices=OPCIONES, widget=widgets.RadioSelectHorizontal())

    pago = models.FloatField()
    plazo = models.StringField()

    op_seleccionada = models.StringField()
    op_seleccionada_ale = models.StringField()
    dec_gan = models.StringField()

    # funcion para que sortea la decision etre A o B
    def sortear_eleccion(self):
        sortear = random.randint(1,2)
        return 'A' if sortear==1 else 'B'

    #se saca la máquina de casa participante
    maquina = models.IntegerField()

    def calcularNumMaquina(self):
        ip = str(self.participant.ip_address)
        if not ip.startswith('200.126.3.'):
            self.maquina = 0
        else:
            maq = int(ip[-3:])
            self.maquina = self.session.vars['dicc_ip'][maq]
