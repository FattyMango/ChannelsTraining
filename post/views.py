from django.shortcuts import render
from .models import Post,Like
from channels.layers import get_channel_layer
from asgiref.sync import AsyncToSync
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.
def index (request):
    user = request.user
    post = Post.objects.get()
    likes = Like.objects.filter(post=post).count()
    context = {
        'likes' : likes,
        'post':post
        }
    return render(request,'post.html',context) 
    
def send_like(request):
    user = request.user
    pk = request.POST.get("pk")
    
    post = Post.objects.get(id = pk)
    try:
        Like.objects.get(post=post)
    except Like.DoesNotExist:
        like = Like.objects.create(user=user,post=post)
    likes = Like.objects.filter(post=post).count()
    channel_layer = get_channel_layer()

    # userto = User.objects.get(id = post.author.pk)

    ''' Basicly what it does is we are giving the (group)
    the data we want 
    and that does not effect any other consumers if we make sure
    that each consumer has different (group name) '''

    AsyncToSync(channel_layer.group_send)(
            str(post.author.pk),
            {"type": "send_message",
            'message':'like sent',
            'username' : user.username,
            
             })

    return HttpResponse(json.dumps({'success':'success','likes':likes})) 
