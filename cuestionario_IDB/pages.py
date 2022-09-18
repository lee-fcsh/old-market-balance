from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Consentimiento(Page):
    form_model = 'player'
    form_fields = ['offer_accepted']


class Quizz_Part1(Page):
    # form_model = 'player'
    # form_fields = ['CI18']
    def is_displayed(self):
        return self.player.offer_accepted
    
    def vars_for_template(self):
        p_1 = "¿Cuánta confianza tiene usted en la Policía?"
        p_2 = "¿Cuánta confianza tiene usted en las escuelas públicas?"
        p_3 = "¿Cuánta confianza tiene usted en los hospitales públicos?"
        p_4 = "¿Cuánta confianza tiene usted en los empleados públicos?"
        p_5 = "¿Cuánta confianza tiene usted en el Congreso/Parlamento?"
        p_6 = "¿Cuánta confianza tiene usted en los jueces?"
        p_7 = "¿Cuánta confianza tiene usted en los empresarios?"
        p_8 = "¿Cuánta confianza tiene usted en los políticos?"

        p_9 = "¿Cree usted que es común que la Policía pueda prevenir el crimen?"
        p_10 = "¿Cree usted que es común que las escuelas públicas ofrezcan una educación de calidad?"
        p_11 = "¿Cree usted que es común que los hospitales públicos ofrezcan servicios de calidad?"
        p_12 = "Si se quejara de la mala calidad de un servicio público, ¿cree usted que el empleado público podría resolver efectivamente el problema?"
        p_13 = "¿Cree usted que es común que los legisladores cumplan con lo que prometen?"
        p_14 = "¿Cree usted que es común que los jueces tomen decisiones justas?"
        p_15 = "¿Cree usted que es común que las empresas ofrezcan productos de calidad a precios justos?"
        p_16 = "¿Cree usted que es común que las Fuerzas Armadas contribuyan a la seguridad pública?"
        p_17 = "¿Cree usted que es común que los políticos piensen en usted y en los intereses de gente como usted?"
        preguntas = [p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8, p_9, p_10, p_11, p_12, p_13, p_14, p_15, p_16, p_17]

        opciones = [i for i in range(1, 11)]
        ids_preg = [i for i in range(1, 18)]

        return {
                'preguntas': preguntas,
                'opciones': opciones,
                'mult': zip(ids_preg, preguntas)
                }

class Quizz_Part2(Page):
    def is_displayed(self):
        return self.player.offer_accepted

    def vars_for_template(self):
        p_1 = "¿Cuánta confianza tiene usted en los extranjeros que viven actualmente en su comunidad?"
        p_2 = "¿Cuánta confianza tiene usted en su familia?"
        p_3 = "¿Cuánta confianza tiene usted en los profesores de la escuela de su(s) hijo/a(s) o de su propia escuela?"
        p_4 = "¿Cuánta confianza tiene usted en los doctores del último hospital que visitó?"
        p_5 = "¿Cuánta confianza tiene usted en la Policía de su barrio?"
        
        preguntas = [p_1, p_2, p_3, p_4, p_5]

        opciones = [i for i in range(1, 11)]
        ids_preg = [i for i in range(1, 5)]

        return {
                'preguntas': preguntas,
                'opciones': opciones,
                'mult': zip(ids_preg, preguntas)
                }


class Quizz_Part3(Page):
    def is_displayed(self):
        return self.player.offer_accepted

    def vars_for_template(self):
        opciones = [i for i in range(1, 11)]

        p_3 = "Los políticos en general"
        p_4 = "Los funcionarios públicos "
        p_5 = "Los empresarios "
        p_6 = "Los miembros de su familia"
        p_7 = "Los policías"
        p_8 = "Los jueces y fiscales"

        preguntas1 = [p_3, p_4, p_5, p_6, p_7, p_8]
        ids_preg1 = [i for i in range(3, 9)]
        ids_preg2 = [i for i in range(9, 15)]
        ids_preg3 = [i for i in range(15, 21)]
        opciones1 = [i for i in range(1, 5)]

        return {
                'preguntas1': preguntas1,
                'opciones': opciones,
                'opciones1': opciones1,
                'mult1': zip(ids_preg1, preguntas1),
                'mult2': zip(ids_preg2, preguntas1),
                'mult3': zip(ids_preg3, preguntas1)
                }


class Quizz_Part4(Page):
    def is_displayed(self):
        return self.player.offer_accepted

    def vars_for_template(self):
        p_5 = "¿Cuán común es que usted se sienta solo?"
        p_6 = "¿Cuán común es que usted sienta que le cuesta hacer amigos?"
        p_7 = "¿Cuán probable sería que, si usted tiene penurias económicas, alguien le preste dinero?"
        p_8 = "¿Cuán probable sería que, si tiene una emergencia de salud, alguien pase la noche en el hospital con usted?"

        preguntas = [p_5, p_6, p_7, p_8]
        ids_preg = [i for i in range(5, 9)]
        opciones = [i for i in range(1, 5)]

        return {
                'preguntas': preguntas,
                'opciones': opciones,
                'mult': zip(ids_preg, preguntas),
                }

class Quizz_Part5(Page):
    def is_displayed(self):
        return self.player.offer_accepted
    
    def vars_for_template(self):
        concp1 = "Ninguno"
        concp2 = "1er curso de primaria"
        concp3 = "2o curso de primaria"
        concp4 = "3er curso de primaria"
        concp5 = "4o curso de primaria"
        concp6 = "5o curso de primaria"
        concp7 = "6o curso de primaria/1ro intermedio"
        concp8 = "1er curso de secundaria/2do intermedio"
        concp9 = "2o curso de secundaria/3ro intermedio"
        concp10 = "3er curso de secundaria/1ro medio"
        concp11 = "4o curso de secundaria/2do medio"
        concp12 = "5o curso de secundaria/3ro medio"
        concp13 = "6o curso de secundaria/4to medio (bachiller)"
        concp14 = "1er curso de universidad/superior no universitaria "
        concp15 = "2o curso de universidad/superior no universitaria "
        concp16 = "3er curso de universidad/superior no universitaria"
        concp17 = "4o curso de universidad/superior no universitaria"
        concp18 = "5o curso de universidad"
        concp19 = "6o curso de universidad o más (Posgrado)"

        preguntas = [concp1, concp2, concp3, concp4, concp5, concp6, concp7, concp8, concp9, concp10, concp11, concp12, concp13, concp14, concp15, concp16, concp17, concp18, concp19]
        ids_preg = [i for i in range(0, 19)]
        opciones = [i for i in range(0, 19)]

        return {
                'preguntas': preguntas,
                'opciones': opciones,
                'mult': zip(ids_preg, preguntas),
                }


page_sequence = [Consentimiento, Quizz_Part1, Quizz_Part2, Quizz_Part3, Quizz_Part4, Quizz_Part5]
