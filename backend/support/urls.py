from django.urls import path
from . import views


urlpatterns = [
    path("orders/<int:order_id>", views.get_order_status),

    path("returns/", views.get_return_categories),
    path("returns/status", views.get_return_status),
    path(
        "returns/<str:category>/check",
        views.check_return_eligibility),
    path("returns/<str:category>", views.get_return_policy),
   
]