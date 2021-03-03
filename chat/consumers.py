import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from .models import Message,Room
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id
        # print((self.room_group_name,self.channel_name))
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        
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
        await self.channel_layer.group_send(

            self.room_group_name,{
               'type':'send_message',
               'message':ms.content,
               'username' : ms.user.username
               
            }
        )
    async def send_message(self,content):
        message = content['message']
        username = content['username']
        
        await self.send(text_data= json.dumps({'message':message,'username':username}))

@database_sync_to_async
def create_message(content,email,recieveremail,roomPk):
    user = User.objects.get(email = email)
    reciever = User.objects.get(email = recieveremail)
    
    try:
        room = Room.objects.get(pk = roomPk)
    except Room.DoesNotExist:
        room = Room.objects.create(user1=user1,user2=user2) 
        # room.save()
    
    return Message.objects.create(content=content,user=user,reciever=reciever,room=room)
    
#fors om,e reason its not working
# @database_sync_to_async
# def get_room_or_create(pk,user1,user2) :
#     print(pk)
#     try:
#         room = Room.objects.get(pk = pk)
#     except Room.DoesNotExist:
#         room = Room.objects.create(user1=user1,user2=user2) 
#         room.save()   
#     return room    

