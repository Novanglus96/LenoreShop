import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sync", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sync", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def sync_invalidate(self, event):
        await self.send(text_data=json.dumps({
            "type": "invalidate",
            "keys": event["keys"],
        }))
