from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path("details", Employees_Details.as_view(), name="details"),
    path('actions/', Actions_View.as_view(), name='actions_view'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/<int:pk>/gallery/', TemplateGalleryView.as_view(), name='template_gallery'),
    path('employee/<int:pk>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('employee/<int:pk>/delete/', DeleteProfileView.as_view(), name='delete_profile'),
    path('employee/delete/<int:pk>', DeleteEmployeeRecord.as_view(), name='employee_delete_record'),
]
 
# from django.contrib import admin
# from django.urls import path,include
# from .views import Employees_Details, Actions_View


# urlpatterns = [
#     path("details", Employees_Details.as_view(), name="details"),
#     path('actions/', Actions_View.as_view(), name='actions_view'),

   

    
# ]