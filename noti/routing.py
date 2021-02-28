from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    path('noti/', consumers.noticonsumer.as_asgi()),
]