from django.contrib import admin
from django.urls import path,include
from .views import NewEmployeeRegister

urlpatterns = [
    path("register/<int:pk>", NewEmployeeRegister.as_view(), name="New_Employee_Registration"),
]
    