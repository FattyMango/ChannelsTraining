from django.shortcuts import render
from .models import notification
# Create your views here.
def index (request):
    user = request.user
    noti = notification.objects.filter(reciever=user)
    context = {}
    context['noti'] = noti
    return render(request,'noti.html',context)
