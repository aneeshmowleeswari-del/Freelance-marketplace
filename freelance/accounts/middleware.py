from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout

class CheckApprovalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Skip approval check for superusers/admin
            if not request.user.is_superuser and not request.user.is_approved:
                messages.error(request, "Your account is not approved by Admin yet.")
                logout(request)
                return redirect("login")

        response = self.get_response(request)
        return response
