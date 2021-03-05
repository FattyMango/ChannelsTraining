
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/',include('chat.urls')),
    path('noti/',include('noti.urls')),
    path('post/',include('post.urls'))
]
