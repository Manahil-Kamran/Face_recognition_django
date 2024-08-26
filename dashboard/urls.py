from django.urls import path
from .views import Main_Dashboard
from .api import *
urlpatterns = [
    path("dashboard", Main_Dashboard, name="index"),


    # api path
    path("api/get_all/face_coding",GetFaceCodingApiView.as_view(),name="get_all_face_coding"),
    path("api/get_face_codings_testknn",GetAllFaceCodingApiView.as_view(),name="get_face_codings_testknn")
]