from django.urls import path 
from .views import PurchaseViews , PurchaseViewsById

urlpatterns = [
    path("purchase_orders/",PurchaseViews.as_view(),name="po"),
    path("purchase_orders/<str:pk>/",PurchaseViewsById.as_view(),name="po_id")

]
