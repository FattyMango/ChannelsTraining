from django.urls import path
from . import views
urlpatterns = [

path('',views.index),
path('send',views.send_noti,name = 'send'),
path('test',views.test)

]