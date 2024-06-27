from django.shortcuts import render

from django.http import HttpResponse

def Main_Dashboard(request):
    if request.method == "GET":
        template_name = "dashboard/index.html"
    if request.method == "POST":
        template_name = "dashboard/index.html"
    return render(request, template_name)