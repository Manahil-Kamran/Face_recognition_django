from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class Report(TemplateView):
    template_name = "reports/reports.html"

    def get(self,request):

        return render(request,self.template_name)

    def post(self,request):
        pass 