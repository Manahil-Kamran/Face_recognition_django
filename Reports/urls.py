from django.urls import path
from .views import Report


urlpatterns = [
    
    path("reports/", Report.as_view(), name="reports"),
 
]