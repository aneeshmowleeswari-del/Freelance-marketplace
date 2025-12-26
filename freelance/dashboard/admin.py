from django.contrib import admin
from .models import Application, Proposal, ProjectSubmission

# Register your models here.





@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'project', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('freelancer__user__username', 'project__title')

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'project', 'bid_amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('freelancer__username', 'project__title')

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('project', 'freelancer', 'review_status', 'submitted_at', 'reviewed_at')
    list_filter = ('review_status',)
    search_fields = ('freelancer__username', 'project__title')
