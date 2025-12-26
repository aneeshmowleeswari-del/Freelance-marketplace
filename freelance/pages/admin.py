from django.contrib import admin
from .models import Category,Project 


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_count')  # will show count in admin
admin.site.register(Category, CategoryAdmin)



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'assigned_freelancer', 'status', 'is_paid')
    list_filter = ('status', 'is_paid', 'category')
    search_fields = ('title', 'client__username', 'assigned_freelancer__username')



