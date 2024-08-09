from django.shortcuts import render
from django.views.generic import TemplateView
from dashboard.models import PersonRegistration

# Create your views here.
class Employees_Details(TemplateView):
    template_name = "details/details.html"
    
    def get(self,request):
        pr= PersonRegistration.objects.all()
        return render(request, self.template_name,{"pr":pr})
# def Employees_Details(request):
#     if request.method == "GET":
#         template_name = "details/details.html"
#     if request.method == "POST":
#         template_name = "details/details.html"
#     return render(request, template_name)
