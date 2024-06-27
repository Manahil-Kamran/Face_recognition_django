from django.contrib import admin
from django.urls import path,include
from .views import Main_Dashboard

urlpatterns = [
    path("dashboard", Main_Dashboard, name="index"),

    
]