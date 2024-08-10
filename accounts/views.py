from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_view(request):
    template_name = "accounts/login.html"
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            login(request, user)
            # Redirect to a success page or dashboard
            return redirect('index')  # Replace 'dashboard' with your actual dashboard URL name
        else:
            # Return an 'invalid login' error message.
            return HttpResponse("Invalid username or password", status=401)
    
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

