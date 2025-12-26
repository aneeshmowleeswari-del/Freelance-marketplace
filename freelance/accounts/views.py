from django.shortcuts import render, redirect,get_object_or_404
from .forms import ClientSignupForm, FreelancerSignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import User, FreelancerProfile, ClientProfile
from pages.models import Category
from payments.models import Payment,Review
from django.db.models import Count


# ==================ADMIN CHECK=======================
def admin_check(user):
    return user.is_authenticated and user.is_staff
#=====================ADMIN DASHBOARD================
@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):
    
    freelancers = FreelancerProfile.objects.select_related('user').all()
    clients = ClientProfile.objects.select_related('user').all()
    categories =Category.objects.annotate(num_projects=Count('projects'))
    payments = Payment.objects.select_related('client', 'freelancer', 'project').all()
    reviews = Review.objects.select_related( "client","freelancer","payment__project").order_by("-created_at")
    
    
    total_payment_amount = sum(p.total_amount for p in payments)
    total_admin_commission = sum(p.admin_amount for p in payments)  # if you have commission field
    total_freelancer_amount = sum(p.freelancer_amount for p in payments) 
    
    context = {
        'freelancers': freelancers,
        'clients': clients,

        'total_users': User.objects.count(),
        'total_clients': User.objects.filter(user_type='client').count(),
        'total_freelancers': User.objects.filter(user_type='freelancer').count(),

        'approved_clients': ClientProfile.objects.filter(user__is_approved=True).count(),
        'pending_clients': ClientProfile.objects.filter(user__is_approved=False).count(),

        'approved_freelancers': FreelancerProfile.objects.filter(user__is_approved=True).count(),
        'pending_freelancers': FreelancerProfile.objects.filter(user__is_approved=False).count(),

        'categories': categories,
        'payments': payments,
        "reviews": reviews,

        'total_payment_amount': total_payment_amount,
        'total_admin_commission': total_admin_commission,
        'total_freelancer_amount': total_freelancer_amount,
        
    
    }
    return render(request, 'accounts/admin_dashboard.html', context)
#===============APPROVE/REJECT============

@login_required
@user_passes_test(admin_check)
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_approved = True
    user.save()
    messages.success(request, "User approved successfully")
    return redirect('admin_dashboard')




@login_required
@user_passes_test(admin_check)
def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_approved = False
    user.save()
    messages.warning(request, "User rejected")
    return redirect('admin_dashboard')

# ================= DELETE USER (CLIENT / FREELANCER) =================
@login_required
@user_passes_test(admin_check)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.user_type in ['client', 'freelancer']:
        user.delete()
        messages.success(request, "User deleted successfully")
    else:
        messages.error(request, "Admin cannot be deleted")

    return redirect('admin_dashboard')




#================SIGNUP=============

def signup_view(request):
    if request.method == "POST":

        user_type = request.POST.get("user_type")  # client or freelancer

        # If user selected Client
        if user_type == "client":
            form = ClientSignupForm(request.POST)
        
        # If user selected Freelancer
        else:
            form = FreelancerSignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False   # <-- REQUIRED (DO NOT REMOVE/CHANGE)
            user.save()

            messages.success(request, "Registration successful. Wait for admin approval.")
            return redirect("login")

    else:
        # default forms when page loads (you can show only one or both)
        cform = ClientSignupForm()
        fform = FreelancerSignupForm()

    return render(request, "accounts/signup.html", {
        "cform": cform,
        "fform": fform
    })


#===============REGISTER CLIENT/FREELANCER==================

def client_register(request):
    if request.method == "POST":
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ClientSignupForm()
    return render(request, 'accounts/client_register.html', {'form': form})
def freelancer_register(request):
    if request.method == "POST":
        form = FreelancerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = FreelancerSignupForm()
    return render(request, 'accounts/freelancer_register.html', {'form': form})

#=================LOGIN===============
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # ✅ ADMIN LOGIN (FIRST)
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')  # or /admin/

            # ✅ NON-ADMIN MUST BE APPROVED
            if not user.is_approved:
                messages.error(request, f"Your {user.user_type} account is not approved yet.")
                return redirect('login')

            # ✅ CLIENT
            if user.user_type == 'client':
                login(request, user)
                return redirect('client_dashboard')

            # ✅ FREELANCER
            elif user.user_type == 'freelancer':
                login(request, user)
                return redirect('freelancer_dashboard')

            else:
                messages.error(request, "Invalid user type!")
                return redirect('login')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'accounts/login.html')
#==================LOGOUT=============

def logout_view(request):
    logout(request)
    return redirect('login')









