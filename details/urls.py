from django.contrib import admin
from django.urls import path,include
from .views import Employees_Details


urlpatterns = [
    path("details", Employees_Details, name="details"),

    
]