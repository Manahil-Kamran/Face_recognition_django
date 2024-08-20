from django.contrib import admin
from django.urls import path,include
from .views import  LiveFeedIn, LiveFeedOut,DeleteALLUnKnowns


urlpatterns = [
    path("IN", LiveFeedIn.as_view(), name="livefeedin"),
    path("OUT", LiveFeedOut.as_view(), name= "livefeedout"),
    path("delete/all/unknowns", DeleteALLUnKnowns, name="delete_all_unknows"),


    
]
