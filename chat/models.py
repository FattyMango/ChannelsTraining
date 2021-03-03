from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Room (models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user1')  
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user2')    
    date_created = models.DateField(auto_now_add=True,blank=True,null=True)  
    def __str__(self):
        return f'{self.user1.username} - {self.user2.username}'

class Message (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user')
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='Reciever',null = True)
    content = models.CharField(max_length=100)
    room = models.ForeignKey(Room,on_delete=models.CASCADE,null=True)
    date_created = models.DateField(auto_now_add=True,blank=True,null=True) 
    def __str__(self):
        return self.content

