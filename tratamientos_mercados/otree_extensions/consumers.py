# tratamientos_mercados/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from termcolor import colored
from tratamientos_mercados.models import Player, Group, Constants, Subsession
import time


class Tratamientos_mercadosConsumer(WebsocketConsumer):
    def connect(self):
        self.group_pk = int(self.scope['url_route']['kwargs']['group_pk'])
        self.player_pk = int(self.scope['url_route']['kwargs']['player_pk'])
        self.room_group_name = 'tratamientos_mercados_%s' % self.group_pk
        self.group = Group.objects.get(pk=self.group_pk)
        self.player = Player.objects.get(pk=self.player_pk)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('bid_up'):
            if self.player.role() == "comprador":
                self.player.oferta = float(text_data_json.get('new_value'))
            else:
                self.player.precio = float(text_data_json.get('new_value'))
            
            self.player.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'new_bid',
                    'price': float(text_data_json.get('new_value')),
                    'id': self.player.identificador,
                    'rol': self.player.role(),
                }
            )
        else:
            id_btn = text_data_json.get('id_btn')
            valor_venta = 0
            for p in self.group.get_players():
                if p.identificador == id_btn:
                    if p.role() == 'comprador':
                        valor_venta = p.oferta
                    else:
                        valor_venta = p.precio
                    break
            
            for p in self.group.get_players():
                if p.identificador == id_btn or p.identificador == self.player.identificador:
                    p.id_venta = id_btn
                    p.valor_venta = valor_venta
                    p.save()
                else:
                    if p.role() == 'comprador':
                        p.oferta = None
                    else:
                        p.precio = None
                    p.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'new_group',
                    'id': self.player.identificador,
                    'id2': text_data_json.get('id_btn'),
                    'valor_venta': valor_venta
                }
            )

    # Receive message from room group
    def new_bid(self, event):
        precio = event['price']
        id = event['id']
        rol = event['rol']
        self.send(text_data=json.dumps({
            'proceso':1,
            'price': precio,
            'id': id,
            'rol': rol,
        }))

    def new_group(self, event):
        id = event['id']
        id2 = event['id2']
        valor_venta = event['valor_venta']
        self.send(text_data=json.dumps({
            'proceso':0,
            'id': id,
            'id2': id2,
            'actualo':0,
            'actualp': 999999999999999999999999999,
            'valor_venta' : valor_venta
        }))
