from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from dashboard.models import PersonRegistration
class Employees_Details(TemplateView):
    template_name = "details/details.html"
    
    def get(self, request):
        pr_list = PersonRegistration.objects.all()
        paginator = Paginator(pr_list, 10)  # Show 10 employees per page

        page_number = request.GET.get('page')
        pr = paginator.get_page(page_number)

        return render(request, self.template_name, {"pr": pr})



# Create your views here.
# class Employees_Details(TemplateView):
#     template_name = "details/details.html"
    
#     def get(self,request):
#         pr= PersonRegistration.objects.all()
#         return render(request, self.template_name,{"pr":pr})
# def Employees_Details(request):
#     if request.method == "GET":
#         template_name = "details/details.html"
#     if request.method == "POST":
#         template_name = "details/details.html"
#     return render(request, template_name)
