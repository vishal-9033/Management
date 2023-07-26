from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class LoginAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_authenticated and user.is_superuser:
            return "/admin"
        elif user.is_authenticated and user.is_staff:
            return "/admin"
        else:
            return "/"