from django.shortcuts import render

# Create your views here.
def LiveStream_in(request):
    if request.method == "GET":
        template_name = "live_stream/streamIN.html"
    if request.method == "POST":
        template_name = "live_stream/streamIN.html"
    return render(request, template_name)
def LiveStream_out(request):
    if request.method == "GET":
        template_name = "live_stream/streamOUT.html"
    if request.method == "POST":
        template_name = "live_stream/streamOUT.html"
    return render(request, template_name)    