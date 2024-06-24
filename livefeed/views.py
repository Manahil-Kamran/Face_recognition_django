from django.shortcuts import render
from django.http import HttpResponse

def LiveFeed_in(request):
    return HttpResponse("Type in to LiveFeed_in")
def LiveFeed_out(request):
    return HttpResponse("TYPE IN TO VIEW LIVEFEED OUT ")
