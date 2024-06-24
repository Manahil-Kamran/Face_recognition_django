from django.shortcuts import render
from django.http import HttpResponse

def LiveFeed_in(request):
    if request.method == "GET":
        template_name = "live_feed/in.html"
    if request.method == "POST":
        template_name = "live_feed/in.html"
    return render(request, template_name)
def LiveFeed_out(request):
    if request.method == "GET":
        template_name = "live_feed/out.html"
    if request.method == "POST":
        template_name = "live_feed/out.html"
    return render(request, template_name)
   