from django.http import JsonResponse
from dashboard.models import PersonRegistration

def employee_search_api(request):
    q = request.GET.get('q', '')
    employees = PersonRegistration.objects.filter(full_name__icontains=q).values('id', 'full_name')[:10]

    data = {
        'results': list(employees),
        'total_count': PersonRegistration.objects.filter(full_name__icontains=q).count()
    }
    return JsonResponse(data)
