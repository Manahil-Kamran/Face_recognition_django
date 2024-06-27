from django.shortcuts import render

# Create your views here.
def Employees_Details(request):
    if request.method == "GET":
        template_name = "details/details.html"
    if request.method == "POST":
        template_name = "details/details.html"
    return render(request, template_name)
