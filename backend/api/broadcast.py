import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger("api")


def broadcast_invalidate(keys: list, group: str = "sync"):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.warning("broadcast_invalidate: no channel layer configured")
        return
    try:
        async_to_sync(channel_layer.group_send)(
            group,
            {"type": "sync.invalidate", "keys": keys},
        )
    except Exception as e:
        logger.warning("broadcast_invalidate failed: %s", e)
