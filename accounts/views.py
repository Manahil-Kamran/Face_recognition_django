from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def login_view(request):
    if request.method == "GET":
        template_name = "accounts/login.html"
    if request.method == "POST":
        template_name = "accounts/livefeed.html"
    return render(request, template_name)
def logout_view(request):
    return HttpResponse("Type in to LOGOUT")
def register_view(request):
    return HttpResponse("Type in to REGISTER")
def profile_view(request):
    return HttpResponse("Type in to view admin PROFILE")

