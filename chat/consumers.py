import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from .models import Message
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,self.channel_name
        )   
    
    def receive(self,text_data):
        text_data_json = json.loads(text_data)
        print("text_data " + text_data)
        message = text_data_json['message']
        email = text_data_json['email']
        ms = create_message(content = message,email = email)
        async_to_sync(self.channel_layer.group_send)(

            self.room_group_name,{
               'type':'send_message',
               'message':ms.content,
               'username' : ms.user.username
            }
        )
    def send_message(self,content):
        message = content['message']
        username = content['username']
        
        self.send(text_data= json.dumps({'message':message,'username':username}))
def create_message(content,email):
    user = User.objects.get(email = email)
    return Message.objects.create(content=content,user=user)