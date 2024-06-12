from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def login_view(request):
    
    return HttpResponse("HELLO LOGIN")
def logout_view(request):
    return HttpResponse("Type in to LOGOUT")
def register_view(request):
    return HttpResponse("Type in to REGISTER")
def profile_view(request):
    return HttpResponse("Type in to view admin PROFILE")

