from django.contrib import admin
from django.urls import path,include
from .views import LiveFeed_out, LiveFeed_in


urlpatterns = [
    path("IN", LiveFeed_in, name="livefeedin"),
    path("OUT", LiveFeed_out, name= "livefeedout"),
    
]