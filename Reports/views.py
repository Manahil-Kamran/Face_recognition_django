from django.shortcuts import render
from django.views.generic import TemplateView
from dashboard.models import PersonAttend
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator

class Report(TemplateView):
    template_name = "reports/reports.html"

    def get(self, request):
        # Get the date range from the request (or default to today)
        start_date_str = request.GET.get('start_date', timezone.now().date().strftime('%Y-%m-%d'))
        end_date_str = request.GET.get('end_date', timezone.now().date().strftime('%Y-%m-%d'))

        # Convert the string dates to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Filter records within the date range
        records = PersonAttend.objects.filter(time_sent__date__range=[start_date, end_date])
        
        # Paginate the records
        paginator = Paginator(records, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "record": page_obj,
            "start_date": start_date_str,
            "end_date": end_date_str
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass
