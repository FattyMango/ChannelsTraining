from django.urls import path
from . import views
urlpatterns = [

    path('',views.index),
    path('send_like',views.send_like,name = 'send_like')
]