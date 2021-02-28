from django.db import models
from django.conf import settings
 
# Create your models here.
class Message (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user')
    content = models.CharField(max_length=100)
    # date_created = models.DateField(auto_now_add=True,blank=True,null=True) 
    def __str__(self):
        return self.content

class Room (models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user1')  
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user2')    
    
    date_created = models.DateField(auto_now_add=True,blank=True,null=True)  