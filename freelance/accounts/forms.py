from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,ClientProfile,FreelancerProfile


class ClientSignupForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=""
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=""
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {'username': '', 'email': ''}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "client"
        if commit:
            user.save()
        return user


class FreelancerSignupForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=""
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=""
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {'username': '', 'email': ''}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "freelancer"
        if commit:
            user.save()
        return user
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['profile_image', 'company_name']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your company name'}),
        }

class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['profile_image', 'skills', 'experience', 'hourly_rate']

        widgets = {
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List your skills separated by commas...'
            }),
            'experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Years of experience'
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01,
                'placeholder': 'Your hourly rate in ₹'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }