from django.contrib import admin
from django.urls import path,include
from .views import LiveFeed_in


urlpatterns = [
    path("", LiveFeed_in, name="livefeedin"),
    
]