from django.shortcuts import render,redirect
from django.db.models import Count
from .models import Category
from django.contrib import messages
from .forms import ContactForm
# Create your views here.
def home(request):
    return render(request,'pages/home.html')
def about(request):
    return render(request,'pages/about.html')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # handle valid form (save data or send email)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # redirect after success
        else:
            # form is invalid, render page again with errors
            return render(request, 'pages/contact.html', {'form': form})
    else:
        form = ContactForm()  # GET request
    return render(request, 'pages/contact.html', {'form': form})

def categories_view(request):
    categories = Category.objects.annotate(project_count=Count('projects'))
    return render(request, 'pages/categories.html', {'categories': categories})
def job_listing(request):
    return render(request, 'pages/job_listing.html')


