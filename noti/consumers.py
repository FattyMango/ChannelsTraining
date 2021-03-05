import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import notification
from django.contrib.auth.models import User
class notiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = str(self.user.pk)
        # print(self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,self.channel_name
        )   
    
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        # print("text_data " + text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        reciever = text_data_json['reciever']
        noti = await create_noti( userfrom=sender,userto=reciever,content=message)
        await self.channel_layer.group_send(

            self.group_name,{
               'type':'send_message',
               'message':message,
               'username' : noti.sender.username,
               
               
            }
        )
    async def send_message(self,content):
        message = content['message']
        username = content['username']
        
        await self.send(text_data= json.dumps({'message':message,'username':username}))
        
@database_sync_to_async           
def  create_noti (userfrom,userto,content):
    
    user1 = User.objects.get(email=userto)
    user2 = User.objects.get(email=userfrom)
    
    return notification.objects.create(reciever=user1,sender=user2,content=content)