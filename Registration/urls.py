from django.contrib import admin
from django.urls import path,include
from .views import Registration

urlpatterns = [
    path("register/", Registration, name="New_Employee_Registration"),
]
    