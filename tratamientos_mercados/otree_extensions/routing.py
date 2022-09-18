from django.urls import re_path

from . import consumers

websocket_routes = [
    re_path(r'tratamientos_mercados/(?P<group_pk>\w+)/(?P<player_pk>\w+)$', consumers.Tratamientos_mercadosConsumer),
]


