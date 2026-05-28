from django.urls import path
from api.consumers import SyncConsumer

websocket_urlpatterns = [
    path("ws/sync/", SyncConsumer.as_asgi()),
]
