from django.urls import path
from . import views

urlpatterns = [
    # AUTH
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # REGISTER
    path('freelancer/register/', views.freelancer_register, name="freelancer_register"),
    path('client/register/', views.client_register, name="client_register"),

    # ===================
    # ADMIN DASHBOARD
    # ===================
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('admin/reject-user/<int:user_id>/', views.reject_user, name='reject_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),

]
