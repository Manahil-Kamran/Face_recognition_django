from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from dashboard.models import PersonRegistration, PersonAttend
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic.edit import UpdateView


class Employees_Details(TemplateView):
    template_name = "details/details.html"
    
    def get(self, request):
        pr_list = PersonRegistration.objects.all()
        paginator = Paginator(pr_list, 10)  # Show 10 employees per page
        page_number = request.GET.get('page')
        pr = paginator.get_page(page_number)
        return render(request, self.template_name, {"pr": pr})

class EmployeeDetailView(TemplateView):
    template_name = "details/employee_detail.html"

    def get(self, request, pk):
        employee = get_object_or_404(PersonRegistration, pk=pk)
        all_employees = PersonRegistration.objects.all().values('id', 'full_name')


        # Get all employees and paginate
        record = PersonAttend.objects.filter(person=employee).all()
        paginator = Paginator(record, 10)  # Show 10 employees per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "employee": employee,
            "record": page_obj, 
            "all_employees": all_employees,  # Pass the paginated page object to the context
        }
        return render(request, self.template_name, context)

# class EmployeeDetailView(TemplateView):
#     template_name = "details/employee_detail.html"

#     def get(self, request, pk):
#         employee = get_object_or_404(PersonRegistration, pk=pk)
#         record = PersonAttend.objects.filter(person=employee).all()
#         all_employees= PersonRegistration.objects.all()
#         context = {
#             "employee": employee,
#             "record":record,
#             "all_employees":all_employees,
#             # "details_url": reverse("employee_detail", args=[pk]),
#             # "template_gallery_url": reverse("template_gallery", args=[pk]),
#             # "edit_profile_url": reverse("edit_profile", args=[pk]),
#             # "delete_profile_url": reverse("delete_profile", args=[pk]),
#         }
#         return render(request, self.template_name, context)
    

class TemplateGalleryView(TemplateView):
    template_name = "details/template_gallery.html"

    def get(self, request, pk):
        employee = get_object_or_404(PersonRegistration, pk=pk)
        return render(request, self.template_name, {"employee": employee})

class EditProfileView(TemplateView):
    template_name = "details/edit_profile.html"

    def get(self, request, pk):
        employee = get_object_or_404(PersonRegistration, pk=pk)
        return render(request, self.template_name, {"employee": employee})

class DeleteProfileView(View):

    def post(self, request, pk):
        employee = get_object_or_404(PersonRegistration, pk=pk)
        employee.delete()
        return HttpResponseRedirect(reverse_lazy('details'))

class DeleteEmployeeRecord(View):

    def post(self, request, pk):
        employee = get_object_or_404(PersonAttend, pk=pk)
        employee.delete()
        return HttpResponseRedirect(reverse_lazy('details'))

# from django.shortcuts import render
# from django.core.paginator import Paginator
# from django.views.generic import TemplateView
# from dashboard.models import PersonRegistration

# class Employees_Details(TemplateView):
#     template_name = "details/details.html"
    
#     def get(self, request):
#         pr_list = PersonRegistration.objects.all()
#         paginator = Paginator(pr_list, 10)  # Show 10 employees per page

#         page_number = request.GET.get('page')
#         pr = paginator.get_page(page_number)

#         return render(request, self.template_name, {"pr": pr})

class Actions_View(TemplateView):
    template_name = "details/actions.html"
    
    def get(self, request):
        # Add any context data you need to pass to the actions.html template
        context = {}
        return render(request, self.template_name, context)
