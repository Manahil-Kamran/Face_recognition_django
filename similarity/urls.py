from django.contrib import admin
from django.urls import path,include
from .views import Similarity_Matrix


urlpatterns = [
    path("similarity", Similarity_Matrix, name="similarity"),
   
    
]