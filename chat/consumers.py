import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from .models import Message,Room
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from noti.consumers import create_noti
class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name =  self.room_id
        self.user = self.scope['user']
        self.user.status = True
        print(self.user)
        # print((self.room_group_name,self.channel_name))
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        self.user.status = False
        await self.channel_layer.group_discard(
            self.room_group_name,self.channel_name
        )   
    
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        # print("text_data " + text_data)
        message = text_data_json['message']
        email = text_data_json['email']
        rec = text_data_json['reciever']
        ms = await create_message(content = message,email = email,recieveremail = rec,roomPk = self.room_id)
        noti = await create_noti( userfrom=ms.user.username,userto=ms.reciever.username,content='message sent')
        await self.channel_layer.group_send(

            self.room_group_name,{
               'type':'send_message',
               'message':ms.content,
               'username' : ms.user.username,
               'noti' : noti.content
               
            }
        )
    async def send_message(self,content):
        message = content['message']
        username = content['username']
        noti = content['noti']
        
        await self.send(text_data= json.dumps({'message':message,'username':username,'noti':noti}))

@database_sync_to_async
def create_message(content,email,recieveremail,roomPk):
    user = User.objects.get(email = email)
    reciever = User.objects.get(email = recieveremail)
    room = get_room_or_create(pk=roomPk,user1=user,user2=reciever)    
    return Message.objects.create(content=content,user=user,reciever=reciever,room=room)
    
def get_room_or_create(pk,user1,user2) :
    
    try:
        room = Room.objects.get(pk = pk)
    except Room.DoesNotExist:
        room = Room.objects.create(user1=user1,user2=user2) 
        room.save()   
    return room    

