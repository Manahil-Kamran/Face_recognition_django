from django.contrib import admin
from django.urls import path,include
from .views import LiveFeed_in, LiveFeed_out


urlpatterns = [
    path("IN", LiveFeed_in, name="livefeedin"),
    path("OUT", LiveFeed_out, name= "livefeedout"),
    
]