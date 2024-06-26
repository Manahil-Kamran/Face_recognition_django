from django.shortcuts import render

# Create your views here.
def Registration (request):
    if request.method == "GET":
        template_name = "registration/register.html"
    if request.method == "POST":
        template_name = "registration/register.html"
    return render(request, template_name)