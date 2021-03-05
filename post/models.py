from django.db import models
from django.conf import settings;
# Create your models here.
class Post (models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    data_created = models.DateField(auto_now_add=True)
class Like (models.Model):
    user =   models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    data_created = models.DateField(auto_now_add=True)