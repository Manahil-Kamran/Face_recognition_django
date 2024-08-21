from django.shortcuts import render
from django.views.generic import TemplateView
from dashboard.models import PersonRegistration,PersonAttend
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.
class NewEmployeeRegister(TemplateView):
    template_name = "registration/register.html"

    def get(self,request,pk):
        person_attend= PersonAttend.objects.get(id=pk)
        return render(request,self.template_name,{"person":person_attend})
    
    def post(self,request,pk):
        person_attend= PersonAttend.objects.get(id=pk)
        register = PersonRegistration.objects.get(id=person_attend.person.id)
        full_name = request.POST.get("full_name")
        department_name = request.POST.get("department_name")
        cnic = request.POST.get("cnic")

        register.full_name = full_name
        register.department_name = department_name
        register.cnic = cnic
        register.save()
        if person_attend.camera_id=="P&D":
            return redirect(reverse("livefeedin"))
        else:
            return redirect(reverse("livefeedout"))