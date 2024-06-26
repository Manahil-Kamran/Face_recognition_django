from django.shortcuts import render

# Create your views here.
def Report(request):
    if request.method == "GET":
        template_name = "reports/reports.html"
    if request.method == "POST":
        template_name = "reports/reports.html"
    return render(request, template_name)
