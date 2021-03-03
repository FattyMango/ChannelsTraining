from django.urls import path
from . import views
urlpatterns= [
    path('',views.index),
    path('room/<str:room_id>/', views.room, name='room'),
    path('create-or-return-private-chat',views.get_private_room_create,name='get_room')
    ]
