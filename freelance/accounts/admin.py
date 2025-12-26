from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ClientProfile, FreelancerProfile


# Register your models here 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "user_type", "is_active", "is_staff","is_approved")
    list_editable=("is_approved",)
    list_filter = ("user_type", "is_approved","is_active", "is_staff")
    search_fields = ("username", "email")
    

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name")
    search_fields = ("user__username", "company_name")

@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "skills_display", "experience", "hourly_rate")
    search_fields = ("user__username", "skills")

    # Custom method to display skills
    def skills_display(self, obj):
        return obj.skills or "-"
    skills_display.short_description = "Skills"










