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
        print((data,userto,userfrom))
        noti = await create_noti(userfrom=userfrom,userto=userto,content = data)
        print(noti)
        await self.send_json(content=json.dumps({
            'content' : noti.content,
            'from' : noti.sender.username
        }))
        

# class noticonsumer(WebsocketConsumer):
#     def connect(self):
        
#         print('Connected')
#         # Join room group
#         self.accept()

#     def disconnect(self, close_code):
#         print('Disconnected')

#     # Receive message from WebSocket
#     def receive(self,text_data):
#         content = json.loads(text_data)
#         data = content['content']
#         userto = content['to_email']
#         userfrom = content['from_email']
#         print((data,userto,userfrom))
#         noti = create_noti(userfrom=userfrom,userto=userto,content = data)
#         print(noti)
#         self.send(text_data=json.dumps({
#             'content' : noti.content,
#             'from' : noti.sender.username
#         }))        

# class noticonsumer(AsyncWebsocketConsumer):
#     async def connect(self):
        
#         print('Connected')
#         # Join room group
#         await self.accept()

#     async def disconnect(self, close_code):
#         print('Disconnected')

#     # Receive message from WebSocket
#     async def receive(self,text_data):
#         content = json.loads(text_data)
#         data = content['content']
#         userto = content['to_email']
#         userfrom = content['from_email']
#         print((data,userto,userfrom))
#         noti = await create_noti(userfrom=userfrom,userto=userto,content = data)
#         print(noti)
#         await self.send(text_data=json.dumps({
#             'content' : noti.content,
#             'from' : noti.sender.username
#         })) 
@database_sync_to_async           
def  create_noti (userfrom,userto,content):
    print('create_noti called')
    user1 = User.objects.get(email=userto)
    user2 = User.objects.get(email=userfrom)
    print('noti created')
    return notification.objects.create(reciever=user1,sender=user2,content=content)