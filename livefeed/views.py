

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from dashboard.models import PersonAttend
from django.core.paginator import Paginator
from django.db.models import Q

class LiveFeedIn(TemplateView):
    template_name= "live_feed/in.html"

    def get(self, request):
        pa_list = PersonAttend.objects.filter(camera_id="P&D").select_related('person')
        
        # Filter knowns and unknowns in Python
        knowns = pa_list.filter(~Q(person__full_name__icontains="unknown"))
        unknowns = pa_list.filter(person__full_name__icontains="unknown")
        
        # Paginate knowns
        paginator_knowns = Paginator(knowns, 10)  # Show 10 employees per page
        page_number_knowns = request.GET.get('knowns_page')
        knowns = paginator_knowns.get_page(page_number_knowns)
        
        # Paginate unknowns
        paginator_unknowns = Paginator(unknowns, 10)  # Show 10 employees per page
        page_number_unknowns = request.GET.get('unknowns_page')
        unknowns = paginator_unknowns.get_page(page_number_unknowns)
        print(len(unknowns))
        
        return render(request, self.template_name, {"knowns": knowns, "unknowns": unknowns})
    
class LiveFeedOut(TemplateView):
    template_name= "live_feed/out.html"

    def get(self, request):
        pa_list = PersonAttend.objects.filter(camera_id="EXIT").select_related('person')
        
        # Filter knowns and unknowns in Python
        knowns = pa_list.filter(~Q(person__full_name__icontains="unknown"))
        unknowns = pa_list.filter(person__full_name__icontains="unknown")
        
        # Paginate knowns
        paginator_knowns = Paginator(knowns, 10)  # Show 10 employees per page
        page_number_knowns = request.GET.get('knowns_page')
        knowns = paginator_knowns.get_page(page_number_knowns)
        
        # Paginate unknowns
        paginator_unknowns = Paginator(unknowns, 10)  # Show 10 employees per page
        page_number_unknowns = request.GET.get('unknowns_page')
        unknowns = paginator_unknowns.get_page(page_number_unknowns)
        print(len(unknowns))
        
        return render(request, self.template_name, {"knowns": knowns, "unknowns": unknowns})


      


# def LiveFeed_in(request):
#     if request.method == "GET":
#         template_name = "live_feed/in.html"

#     if request.method == "POST":
#         template_name = "live_feed/in.html"
#     return render(request, template_name)
def LiveFeed_out(request):
    if request.method == "GET":
        template_name = "live_feed/out.html"
    if request.method == "POST":
        template_name = "live_feed/out.html"
    return render(request, template_name)
   