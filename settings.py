from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ADMIN_USERNAME = 'admin'

SESSION_CONFIG_DEFAULTS = dict(
   real_world_currency_per_point=1.00, participation_fee=2.50, doc=""
)

SESSION_CONFIGS = [
    dict(
       name='market',
       display_name="Equilibrio de Mercado (Live)",
       num_demo_participants=2,
       app_sequence=['Welcome2', 'Bienvenida_v2','market_equilibrio', 'tratamientos_mercados','Trust_Game_LEE', 'results_matrix', 'caution_form','cuest_aversion_al_riesgo','cuest_demografico','Goodbye']
    ),
    dict(
       name='Session1',
       display_name="Cuestionarios (P2)",
       num_demo_participants=2,
       app_sequence=['Welcome2', 'Bienvenida_v2','bret','mpl_para_tiempoV2','Trust_Game_LEE','cuestionario_IDB','cuest_aversion_al_riesgo','cuest_demografico','Goodbye']
    ),
    dict(
       name='leetest',
       display_name="TEST GAME",
       num_demo_participants=2,
       app_sequence=['Trust_Game_LEE', 'results_matrix']
    )
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '(nzey0oxy!5b(^n&^*xlqd=eq-41$yuux4_ed@gahl2lnu6+%j'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
EXTENSION_APPS = ['market_equilibrio', 'tratamientos_mercados']
 