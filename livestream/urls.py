from django.contrib import admin
from django.urls import path,include
from .views import LiveStream_in, LiveStream_out

urlpatterns = [
    path("streamIN/", LiveStream_in, name="StreamIN"),
    path("streamOUT/", LiveStream_out, name="StreamOUT"),
    
]