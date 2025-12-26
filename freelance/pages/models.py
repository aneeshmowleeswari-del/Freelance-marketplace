from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def project_count(self):
        # Automatically count related projects
        return self.project_set.count()

    project_count.fget.short_description = "Projects"

class Project(models.Model):
    client = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='projects',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    deadline = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("Open", "Open"),
            ("Assigned", "Assigned"),
            ("Completed", "Completed"),
        ],
        default="Open"
    )

    # 🔽 ADD THESE TWO
    assigned_freelancer = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_projects"
    )
    is_paid = models.BooleanField(default=False)

    attachment = models.FileField(upload_to="project_files/", blank=True, null=True)

    def __str__(self):
        return self.title
