import channels.layers

from django.conf import settings
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            settings.CHANNEL_NAME, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            settings.CHANNEL_NAME, self.channel_name
        )

    notify = lambda self, event: self.send_json(event)


def broadcast_websocket_data(data):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(settings.CHANNEL_NAME, {'type': 'notify'} | data)
