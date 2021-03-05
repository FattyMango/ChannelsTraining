"""
ASGI config for train project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
import chat.consumers
import noti.consumers
from django.urls import re_path,path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'train.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            [
            path('room/<room_id>/', chat.consumers.ChatConsumer.as_asgi()),
            path('noti/', noti.consumers.notiConsumer.as_asgi()),

            ]
        )
    ),
})

