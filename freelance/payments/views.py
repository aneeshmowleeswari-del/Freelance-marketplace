from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment,Review
from django.contrib.auth import get_user_model
from pages.models import Project
from django.contrib.auth import get_user_model


User = get_user_model()




@login_required
def create_payment(request, project_id, freelancer_id):
    freelancer = get_object_or_404(User, id=freelancer_id)
    project = get_object_or_404(Project, id=project_id)

    # prevent duplicate payment
    if Payment.objects.filter(project=project, freelancer=freelancer).exists():
        messages.warning(
            request, "Payment already completed for this project."
        )
        return redirect("view_project", pk=project.id)

    if request.method == "POST":
        amount = request.POST.get("amount")

        if not amount:
            messages.error(request, "Amount is required")
            return redirect(
                "create_payment",
                project_id=project.id,
                freelancer_id=freelancer.id
            )

        payment = Payment.objects.create(
            client=request.user,
            freelancer=freelancer,
            project=project,
            total_amount=Decimal(amount),
            payment_status="completed"
        )

        messages.success(request, "Payment completed successfully")

        # ✅ REDIRECT TO REVIEW PAGE
        return redirect("add_review", payment_id=payment.id)

    return render(
        request,
        "payments/create_payment.html",
        {
            "freelancer": freelancer,
            "project": project,
            "amount": project.budget,
        }
    )

@login_required
def add_review(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        client=request.user,
        payment_status="completed"
    )

    # prevent duplicate review
    if Review.objects.filter(payment=payment).exists():
        messages.info(request, "You already submitted a review.")
        return redirect("view_project", pk=payment.project.id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        feedback = request.POST.get("feedback")

        if not rating or not feedback:
            messages.error(request, "All fields are required.")
            return redirect("add_review", payment_id=payment.id)

        Review.objects.create(
            payment=payment,
            client=request.user,
            freelancer=payment.freelancer,
            rating=rating,
            feedback=feedback
        )

        messages.success(request, "Thank you for your review!")
        # Redirect to project page or dashboard instead of payment_detail
        return redirect("view_project", pk=payment.project.id)

    return render(
        request,
        "payments/add_review.html",
        {"payment": payment}
    )


