from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ADMIN_USERNAME = 'admin'

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

SESSION_CONFIGS = [
    dict(
       name='Session2',
       display_name="Session2",
       num_demo_participants=4,
       app_sequence=['Bienvenida_v2','market_equilibrio', 'tratamientos_mercados','Trust_Game_LEE','cuest_aversion_al_riesgo','cuest_demografico','despedida']
    ),
    dict(
       name='Session1',
       display_name="Session1",
       num_demo_participants=2,
       app_sequence=['Bienvenida_v2','bret','mpl_para_tiempoV2','Trust_Game_LEE','cuestionario_IDB','cuest_aversion_al_riesgo','cuest_demografico','despedida']
    ),
    dict(
       name='TEST',
       display_name="TEST",
       num_demo_participants=4,
       app_sequence=['market_equilibrio']
    ),
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '(nzey0oxy!5b(^n&^*xlqd=eq-41$yuux4_ed@gahl2lnu6+%j'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
EXTENSION_APPS = ['market_equilibrio', 'tratamientos_mercados']
