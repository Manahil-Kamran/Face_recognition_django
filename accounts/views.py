from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def login_view(request):
    if request.method == "GET":
        template_name = "accounts/login.html"
    if request.method == "POST":
        template_name = "accounts/livefeed.htlm"
    return render(request, template_name)
def logout_view(request):
    template_name = "accounts/logout.html"
    return render(request, template_name)
def register_view(request):
    if request.method == "GET":
        template_name = "accounts/register.html"
    if request.method == "POST":
        template_name = "accounts/register.html"
    return render(request, template_name)
def profile_view(request):
    template_name = "accounts/userprofile.html"
    return render(request, template_name)

