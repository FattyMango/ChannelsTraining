import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer,WebsocketConsumer,AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import notification
from django.contrib.auth.models import User

class noticonsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        
        print('Connected')
        # Join room group
        await self.accept()

    async def disconnect(self, close_code):
        print('Disconnected')

    # Receive message from WebSocket
    async def receive_json(self,content):
        data = content.get('content',None)
        userto = content.get('to_email',None)
        userfrom = content.get('from_email',None)
        
        noti = await create_noti(userfrom=userfrom,userto=userto,content = data)
        
        await self.send_json(content=json.dumps({
            'content' : str(noti.content),
            'from' : str(noti.sender.username),
            'time' : str(noti.date_created)
        }))
        
@database_sync_to_async           
def  create_noti (userfrom,userto,content):
    print('create_noti called')
    user1 = User.objects.get(email=userto)
    user2 = User.objects.get(email=userfrom)
    print('noti created')
    return notification.objects.create(reciever=user1,sender=user2,content=content)