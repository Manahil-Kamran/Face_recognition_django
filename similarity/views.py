from django.shortcuts import render

# Create your views here.
def Similarity_Matrix(request):
    if request.method == "GET":
        template_name = "similarity/similarity.html"
    if request.method == "POST":
        template_name = "similarity/similarity.html"
    return render(request, template_name)