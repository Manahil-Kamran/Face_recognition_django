from django.contrib import admin
from django.urls import path,include
from .views import LiveFeedIn, LiveFeed_out


urlpatterns = [
    path("IN", LiveFeedIn.as_view(), name="livefeedin"),
    path("OUT", LiveFeed_out, name= "livefeedout"),
    
]