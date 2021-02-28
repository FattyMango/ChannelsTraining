from django.db import models
from django.conf import settings
# Create your models here.
class notification (models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sender',null = False,blank=False)
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reciever',null = False,blank=False)
    content = models.CharField(max_length=100,null= False,blank=False)    
    def __str__(self):
        return f'({self.reciever}) : {self.content}'