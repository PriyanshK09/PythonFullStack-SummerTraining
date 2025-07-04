from django.urls import re_path
from . import consumers
from . import crypto_consumers

websocket_urlpatterns = [
    re_path(r'ws/stock/$', consumers.StockConsumer.as_asgi()),
    re_path(r'ws/crypto/$', crypto_consumers.CryptoConsumer.as_asgi()),
]