from django.urls import path
from . import views

urlpatterns = [
    path("pay/<int:project_id>/<int:freelancer_id>/", views.create_payment, name="create_payment"),
    path("review/<int:payment_id>/",views.add_review,name="add_review"),
    # path("payment/<int:payment_id>/", views.payment_detail, name="payment_detail"),
    
    
]
