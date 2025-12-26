from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    is_approved = models.BooleanField(default=False)
    # ADD THIS FOR ADMIN APPROVAL
    

    def save(self,*args,**kwargs):
        if self.is_superuser:
            self.user_type = 'admin'
            self.is_approved = True
        super().save(*args, **kwargs)
       

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return f"Client: {self.user.username}"


class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.TextField(null=True,blank=True)
    experience = models.IntegerField(null=True,blank=True)  
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"Freelancer: {self.user.username}"
    
@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'freelancer':
            FreelancerProfile.objects.create(user=instance)
        elif instance.user_type == 'client':
            ClientProfile.objects.create(user=instance)