

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from dashboard.models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse


class LiveFeedIn(TemplateView):
    template_name= "live_feed/in.html"

    def get(self, request):
        pa_list = PersonAttend.objects.filter(camera_id="P&D").select_related('person')
        
        # Filter knowns and unknowns in Python
        knowns = pa_list.filter(~Q(person__full_name__icontains="unknown"))
        unknowns = pa_list.filter(person__full_name__icontains="unknown")
        
        # Paginate knowns
        paginator_knowns = Paginator(knowns, 10)  # Show 10 employees per page
        page_number_knowns = request.GET.get('page')
        knowns = paginator_knowns.get_page(page_number_knowns)
        
        # Paginate unknowns
        paginator_unknowns = Paginator(unknowns, 10)  # Show 10 employees per page
        page_number_unknowns = request.GET.get('page')
        unknowns = paginator_unknowns.get_page(page_number_unknowns)
        
        
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
        page_number_knowns = request.GET.get('page')
        knowns = paginator_knowns.get_page(page_number_knowns)
        
        # Paginate unknowns
        paginator_unknowns = Paginator(unknowns, 10)  # Show 10 employees per page
        page_number_unknowns = request.GET.get('page')
        unknowns = paginator_unknowns.get_page(page_number_unknowns)
        
        
        return render(request, self.template_name, {"knowns": knowns, "unknowns": unknowns})

from django.http import HttpResponseBadRequest

def DeleteALLUnKnowns(request):
    camera_id = request.GET.get("camera_id")
    if not camera_id:
        return HttpResponseBadRequest("Missing camera_id parameter.")

    # Step 1: Filter PersonAttend records based on camera_id and unknown persons
    unknown_attend_records = PersonAttend.objects.filter(
        camera_id=camera_id, person__full_name__icontains="unknown"
    ).select_related('person')

    # Step 2: Collect PersonRegistration IDs for deletion
    unknown_person_ids = unknown_attend_records.values_list('person_id', flat=True)

    # Step 3: Delete corresponding PersonAttend records
    unknown_attend_records.delete()

    # Step 4: Delete the associated PersonRegistration records
    PersonRegistration.objects.filter(id__in=unknown_person_ids).delete()

    # Redirect based on camera_id
    if camera_id == "P&D":
        return redirect(reverse("livefeedin"))
    else:
        return redirect(reverse("livefeedout"))


   