from django.db import models
from accounts.models import FreelancerProfile
from pages.models import Project
from django.conf import settings
from django.utils import timezone

 


# Create your models here.


class Application(models.Model):
    freelancer = models.ForeignKey(
        FreelancerProfile, on_delete=models.CASCADE, related_name='applications'
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='applications'
    )
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')  # pending, accepted, rejected
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.freelancer.user.username} applied for {self.project.title}"


class Proposal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="proposals")
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.freelancer.username} → {self.project.title}"


 # make sure this import works

class ProjectSubmission(models.Model):
    REVIEW_CHOICES = [
        ('pending', 'Pending'),
        ('revision', 'Needs Improvement'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='submissions')
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='freelancer_submissions')

    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    message = models.TextField(blank=True)
    review_status = models.CharField(max_length=20, choices=REVIEW_CHOICES, default='pending')
    client_feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def mark_reviewed(self, status, feedback=''):
        self.review_status = status
        self.client_feedback = feedback
        self.reviewed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.project.title} - {self.freelancer.username} - {self.review_status}"



