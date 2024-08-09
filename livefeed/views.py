from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView



# class LiveFeedIn(TemplateView):
#     template_name = "live_feed/in.html"
    
#     def get(self,request):
#         pr= PersonRegistration.objects.all()
#         return render(request, self.template_name,{"pr":pr})
    
#     def post(self,request):
#         pass
#     def post(self,request):
#         pass


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
   