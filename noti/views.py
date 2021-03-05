from django.shortcuts import render
from django.http import HttpResponse
from .models import notification
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import AsyncToSync
import json
# Create your views here.
def test (request):
    return render(request,'noti.html')
def index (request):
    accounts = User.objects.all()
    return render(request,'nindex.html',{'accounts':accounts})
def send_noti(request):
    user = request.user
    pk = request.POST.get("pk")
    # userto = User.objects.get(id = pk)
    channel_layer = get_channel_layer()
    
    AsyncToSync(channel_layer.group_send)(
            pk,
            {"type": "send_message",
            'message':'message sent',
            'username' : user.username,
            
             })
    return HttpResponse(json.dumps({'success':'success'}))         