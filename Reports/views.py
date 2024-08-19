from django.shortcuts import render
from django.views.generic import TemplateView
from dashboard.models import PersonAttend, PersonRegistration
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Min, Max

class Report(TemplateView):
    template_name = "reports/reports.html"

    def get(self, request):
        # Get the date range from the request (or default to today)
        start_date_str = request.GET.get('start_date', timezone.now().date().strftime('%Y-%m-%d'))
        end_date_str = request.GET.get('end_date', timezone.now().date().strftime('%Y-%m-%d'))

        # Convert the string dates to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Filter and annotate records within the date range
        first_seen = PersonAttend.objects.filter(
            time_sent__date__range=[start_date, end_date]
        ).values('person_id').annotate(
            first_seen_time=Min('time_sent'),
            last_seen_time=Max('time_sent')
        ).order_by('first_seen_time')

        # Fetch full details for the first and last seen records
        person_data = []
        for record in first_seen:
            person = PersonRegistration.objects.get(id=record['person_id'])
            first_record = PersonAttend.objects.filter(
                person=person, time_sent=record['first_seen_time']
            ).first()
            last_record = PersonAttend.objects.filter(
                person=person, time_sent=record['last_seen_time']
            ).first()

            person_data.append({
                "id": person.id,
                "full_name": person.full_name,
                "first": {
                    "id": first_record.id,
                    "img_url": first_record.img_url,
                    "camera_id": first_record.camera_id,
                    "time_sent": first_record.time_sent
                    },
                "last": {
                    "id": last_record.id,
                    "img_url": last_record.img_url,
                    "camera_id": last_record.camera_id,
                    "time_sent": last_record.time_sent
                }
            })

        # Paginate the person_data list
        paginator = Paginator(person_data, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "record": page_obj,
            "start_date": start_date_str,
            "end_date": end_date_str
        }
        return render(request, self.template_name, context)
