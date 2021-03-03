from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    path('room/<room_id>/', consumers.ChatConsumer.as_asgi()),
]