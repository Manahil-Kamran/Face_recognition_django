from django.contrib import admin
from django.urls import path,include
from .views import Report


urlpatterns = [
    
    path("reports/", Report, name="reports"),
 
]