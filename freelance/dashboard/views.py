from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import ClientProfile, FreelancerProfile
from accounts.forms import ClientProfileForm, FreelancerProfileForm
from pages.models import Project
from .models import Proposal, ProjectSubmission
from .forms import ProjectForm, ProposalForm
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User, FreelancerProfile
from django.db.models import Avg
from payments.models import Review 





# =====================================================
# CLIENT DASHBOARD
# =====================================================
@login_required
def client_dashboard(request):
    if request.user.user_type != "client":
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")
    

    profile, created = ClientProfile.objects.get_or_create(
        user=request.user
    )

    total_projects = Project.objects.filter(client=request.user).count()
    active_projects = Project.objects.filter(
        client=request.user,
        proposals__status="approved"
    ).distinct().count()
    completed_projects = Project.objects.filter(
        client=request.user,
        proposals__status="completed"
    ).distinct().count()

    recent_projects = Project.objects.filter(client=request.user).order_by("-created_at")[:5]

    return render(request, "dashboard/client_dashboard.html", {
        "profile": profile,
        "total_projects": total_projects,
        "active_projects": active_projects,
        "completed_projects": completed_projects,
        "recent_projects": recent_projects,
    })


# =====================================================
# EDIT PROFILE (CLIENT & FREELANCER)
# =====================================================
@login_required
def edit_profile(request):

    # ---------- CLIENT ----------
    if request.user.user_type == "client":
        profile, created = ClientProfile.objects.get_or_create(
            user=request.user
        )
        form_class = ClientProfileForm
        redirect_url = "client_dashboard"

    # ---------- FREELANCER ----------
    elif request.user.user_type == "freelancer":
        profile, created = FreelancerProfile.objects.get_or_create(
            user=request.user
        )
        form_class = FreelancerProfileForm
        redirect_url = "freelancer_dashboard"

    # ---------- INVALID USER ----------
    else:
        messages.error(request, "Invalid user type.")
        return redirect("home")

    # ---------- FORM HANDLING ----------
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect(redirect_url)
    else:
        form = form_class(instance=profile)

    return render(request, "dashboard/edit_profile.html", {
        "form": form,
        "profile": profile
    })


# =====================================================
# ADD / EDIT / DELETE PROJECT (CLIENT)
# =====================================================
@login_required
def add_project(request):
    if request.user.user_type != "client":
        return redirect("home")

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            return redirect("client_dashboard")
    else:
        form = ProjectForm()

    return render(request, "dashboard/project_crud.html", {"form": form})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, id=pk, client=request.user)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("client_dashboard")
    else:
        form = ProjectForm(instance=project)

    return render(request, "dashboard/project_crud.html", {
        "project": project,
        "form": form,
        "mode": "edit"
    })


@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, id=pk, client=request.user)

    if request.method == "POST":
        project.delete()
        return redirect("client_dashboard")

    return render(request, "dashboard/project_crud.html", {
        "project": project,
        "mode": "delete"
    })


# =====================================================
# VIEW & APPROVE PROPOSALS (CLIENT)
# =====================================================
@login_required
def view_proposals(request, project_id):
    project = get_object_or_404(Project, id=project_id, client=request.user)
    proposals = Proposal.objects.filter(project=project)

    return render(request, "dashboard/view_proposals.html", {
        "project": project,
        "proposals": proposals,
    })


@login_required
def approve_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)

    if proposal.project.client != request.user:
        return redirect("home")

    proposal.status = "approved"
    proposal.save()

    Proposal.objects.filter(
        project=proposal.project
    ).exclude(id=proposal_id).update(status="rejected")

    messages.success(request, "Proposal approved successfully!")
    return redirect("view_proposals", project_id=proposal.project.id)


@login_required
def reject_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)

    if proposal.project.client != request.user:
        return redirect("home")

    proposal.status = "rejected"
    proposal.save()

    messages.success(request, "Proposal rejected.")
    return redirect("view_proposals", project_id=proposal.project.id)


# =====================================================
# FREELANCER DASHBOARD
# =====================================================
@login_required
def freelancer_dashboard(request):
    if request.user.user_type != "freelancer":
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")
    


    profile, created = FreelancerProfile.objects.get_or_create(
        user=request.user
    )

    # profile = FreelancerProfile.objects.filter(user=request.user).first()
    # if not profile:
    #     messages.error(request, "Freelancer profile not found. Please contact admin.")
    #     return redirect("login")

    search_query = request.GET.get('search', '')
    available_projects = Project.objects.filter(status="Open")

    if search_query:
        available_projects = available_projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    approved_proposals = Proposal.objects.filter(
        freelancer=request.user,
        status="approved"
    ).select_related("project")

    approved_projects = []
    for p in approved_proposals:
        has_submitted = ProjectSubmission.objects.filter(
            project=p.project,
            freelancer=request.user
        ).exists()
        approved_projects.append({
            "project": p.project,
            "has_submitted": has_submitted
        })

    return render(request, "dashboard/freelancer_dashboard.html", {
        "freelancer": profile,
        "available_projects": available_projects,
        "approved_projects": approved_projects,
    })


# =====================================================
# APPLY PROJECT (FREELANCER)
# =====================================================
@login_required
def apply_project(request, project_id):
    if request.user.user_type != "freelancer":
        return redirect("home")

    project = get_object_or_404(Project, id=project_id)

    if Proposal.objects.filter(project=project, freelancer=request.user).exists():
        messages.error(request, "You already applied for this project.")
        return redirect("freelancer_dashboard")

    if request.method == "POST":
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.project = project
            proposal.freelancer = request.user
            proposal.save()
            messages.success(request, "Proposal submitted successfully!")
            return redirect("freelancer_dashboard")
    else:
        form = ProposalForm()

    return render(request, "dashboard/apply_project.html", {
        "project": project,
        "form": form
    })
#======================================================
#     SUBMISSION 
# =====================================================


@login_required
def submission_page(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # ✅ Only freelancer allowed
    if request.user.user_type != "freelancer":
        return HttpResponseForbidden("Only freelancers can submit work.")

    # ✅ Freelancer must be approved for this project
    approved = Proposal.objects.filter(
        project=project,
        freelancer=request.user,
        status="approved"
    ).exists()

    if not approved:
        return HttpResponseForbidden("You are not approved for this project.")

    # ✅ Latest submission (for resubmission)
    submission = ProjectSubmission.objects.filter(
        project=project,
        freelancer=request.user
    ).order_by("-submitted_at").first()

    if request.method == "POST":
        file = request.FILES.get("file")
        github_link = request.POST.get("github_link")
        live_link = request.POST.get("live_link")
        message = request.POST.get("message")

        ProjectSubmission.objects.create(
            project=project,
            freelancer=request.user,
            file=file,
            github_link=github_link,
            live_link=live_link,
            message=message,
            review_status="pending"
        )

        return redirect("view_freelancer_project", pk=project.id)

    return render(request, "dashboard/submission_page.html", {
        "project": project,
        "submission": submission,
    })


# =====================================================
# FREELANCER PROJECT VIEW (SUBMIT WORK)
# =====================================================
@login_required
def freelancer_project_view(request, pk):
    project = get_object_or_404(Project, id=pk)

    if request.user.user_type != "freelancer":
        return redirect("home")

    approved = Proposal.objects.filter(
        project=project,
        freelancer=request.user,
        status="approved"
    ).exists()

    if not approved:
        return HttpResponseForbidden("You are not allowed to submit this project.")

    submission = ProjectSubmission.objects.filter(
        project=project,
        freelancer=request.user
    ).order_by("-submitted_at").first()

    if request.method == "POST":
        ProjectSubmission.objects.create(
            project=project,
            freelancer=request.user,
            file=request.FILES.get("file"),
            github_link=request.POST.get("github_link"),
            live_link=request.POST.get("live_link"),
            message=request.POST.get("message"),
        )
        return redirect("view_freelancer_project", pk=project.id)

    return render(request, "dashboard/freelancer_project.html", {
        "project": project,
        "submission": submission,
    })


# =====================================================
# CLIENT PROJECT VIEW (REVIEW SUBMISSION)
# =====================================================

@login_required
def client_project_view(request, pk):
    # Client can access ONLY their own project
    project = get_object_or_404(Project, id=pk, client=request.user)

    # Latest submission
    submission = ProjectSubmission.objects.filter(
        project=project
    ).order_by("-submitted_at").first()

    if request.method == "POST" and submission:

        # 🔒 Do not allow review again if already final
        if submission.review_status in ["accepted", "rejected"]:
            return redirect("view_project", pk=project.id)

        action = request.POST.get("action")
        feedback = request.POST.get("client_feedback", "").strip()

        # ✅ Validate action
        if action == "accept":
            submission.mark_reviewed("accepted", feedback)

        elif action == "revision":
            submission.mark_reviewed("revision", feedback)

        elif action == "reject":
            submission.mark_reviewed("rejected", feedback)

        return redirect("view_project", pk=project.id)

    return render(request, "dashboard/client_project_detail.html", {
        "project": project,
        "submission": submission,
    })


# =======================
# CLIENT REVIEW VIEW
# ==============


@login_required
def review_submission(request, submission_id):
    submission = get_object_or_404(ProjectSubmission, id=submission_id)

    # ✅ Only client can review
    if not hasattr(request.user, 'clientprofile'):
        return redirect('client_dashboard')

    if request.method == "POST":
        status = request.POST.get("status")
        feedback = request.POST.get("feedback", "")

        submission.mark_reviewed(status, feedback)

    return redirect('view_project', pk=submission.project.id)






# ============================================
#  ADMIN DASHBOARD
# ======================



# Only allow admin users
def admin_check(user):
    return user.is_authenticated and user.user_type == 'admin' and user.is_staff

@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):
    freelancers = FreelancerProfile.objects.select_related('user').all()
    
    context = {
        'freelancers': freelancers,
        'total_users': User.objects.count(),
        'total_clients': User.objects.filter(user_type='client').count(),
        'total_freelancers': User.objects.filter(user_type='freelancer').count(),
        'approved_freelancers': FreelancerProfile.objects.filter(user__is_approved=True).count(),
        'pending_freelancers': FreelancerProfile.objects.filter(user__is_approved=False).count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
@user_passes_test(admin_check)
def approve_freelancer(request, user_id):
    freelancer_user = get_object_or_404(User, id=user_id, user_type='freelancer')
    freelancer_user.is_approved = True
    freelancer_user.save()
    return redirect('admin_dashboard')





# =====================================================
# VIEW FREELANCER PROFILE (READ ONLY - CLIENT SIDE)
# =====================================================
@login_required
def view_freelancer_profile(request, freelancer_id):
    freelancer_user = get_object_or_404(User,id=freelancer_id,user_type="freelancer")

    freelancer_profile = get_object_or_404(FreelancerProfile,user=freelancer_user)
    reviews = Review.objects.filter(freelancer=freelancer_user).order_by("-created_at")

    # ✅ calculate average rating
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    return render(request,"dashboard/view_freelancer_profile.html",{
        "freelancer_user": freelancer_user,
        "freelancer_profile": freelancer_profile,
        "reviews":reviews,
        "avg_rating":avg_rating,
        })
