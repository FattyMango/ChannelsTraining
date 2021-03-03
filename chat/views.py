from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Room,Message
import json
from django.http import HttpResponse
# Create your views here.
def index (request):
    accounts = User.objects.all()
    return render(request,'index.html',{'accounts':accounts})
def room(request, room_id):
    user = request.user
    room = Room.objects.get(pk=room_id)
    if user == room.user1 or user == room.user2:
        if user == room.user1:
            reciever = room.user2
        else:
            reciever = room.user1
    
        return render(request, 'room.html', {
            'room_id': room_id,
            'messages':Message.objects.filter(room=room),
            'reciever':reciever
        })
    else  :
        return HttpResponse('u r not authenticated')  
def get_private_room_create(request,*args,**kwargs):
    user1 = request.user
    payload = {}
    if user1.is_authenticated:
        if request.method == "POST":
            user2_id = request.POST.get("user2_id")
            try:
                user2 = User.objects.get(pk=user2_id)
                room = find_or_create_room(user1, user2)
                payload['response'] = "Successfully got the chat."
                payload['room_id'] = room.id
            except User.DoesNotExist:
                payload['response'] = "Unable to start a chat with that user."
    else:
        payload['response'] = "You can't start a chat if you are not authenticated."
    return HttpResponse(json.dumps(payload), content_type="application/json")

def find_or_create_room(user1,user2):
    try:
        room = Room.objects.get(user1=user1,user2=user2)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(user1=user2,user2=user1)
        except Room.DoesNotExist:
            room = Room(user1=user1,user2=user2)
            room.save()
    return room        
