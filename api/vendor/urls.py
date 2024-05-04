from django.urls import path 
from .views import VendorView , VendorViewById

urlpatterns = [
    # path("vendors/<int:pk>",VendorListCreateUpdateDeleteView.as_view(),name="vendor-details"),
    path("vendors/",VendorView.as_view(),name="vendor"),
    path("vendors/<int:pk>/",VendorViewById.as_view(),name="vendor_id")

]
