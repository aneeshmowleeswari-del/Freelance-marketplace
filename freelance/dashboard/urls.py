from django.urls import path
from . import views

urlpatterns = [

    # CLIENT
    path("client/dashboard/", views.client_dashboard, name="client_dashboard"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),

    # PROJECT CRUD (CLIENT)
    path("project/add/", views.add_project, name="add_project"),
    path("project/edit/<int:pk>/", views.edit_project, name="edit_project"),
    path("project/delete/<int:pk>/", views.delete_project, name="delete_project"),

    # CLIENT PROJECT VIEW (renamed to 'view_project' for clarity)
    path("client/project/<int:pk>/", views.client_project_view, name="view_project"),
    # CLIENT REVIEW VIEW
    path("submission/review/<int:submission_id>/",views.review_submission,name="review_submission"),

    # PROPOSALS
    path("project/<int:project_id>/proposals/", views.view_proposals, name="view_proposals"),
    path("proposal/<int:proposal_id>/approve/", views.approve_proposal, name="approve_proposal"),
    path("proposal/<int:proposal_id>/reject/", views.reject_proposal, name="reject_proposal"),

    # FREELANCER
    path("freelancer/dashboard/", views.freelancer_dashboard, name="freelancer_dashboard"),
    path("project/<int:project_id>/apply/", views.apply_project, name="apply_project"),

    # FREELANCER PROJECT VIEW (renamed to 'view_freelancer_project' for clarity)
    path("freelancer/project/<int:pk>/", views.freelancer_project_view, name="view_freelancer_project"),
    path("freelancer/project/<int:project_id>/submit/", views.submission_page, name="submission_page"),


    # VIEW FREELANCER PROFILE (CLIENT SIDE - READ ONLY)
    path("freelancer/profile/<int:freelancer_id>/",views.view_freelancer_profile,name="view_freelancer_profile"),

]
