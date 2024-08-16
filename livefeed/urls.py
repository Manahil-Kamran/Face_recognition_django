from django.contrib import admin
from django.urls import path,include
from .views import  LiveFeedIn, LiveFeedOut


urlpatterns = [
    path("IN", LiveFeedIn.as_view(), name="livefeedin"),
    path("OUT", LiveFeedOut.as_view(), name= "livefeedout"),
    
]
