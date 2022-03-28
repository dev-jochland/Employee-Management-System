from dj_rest_auth.views import LogoutView
from rest_framework.permissions import IsAuthenticated


class CustomLogoutView(LogoutView):
    """View only accessible to logged in users and invalidates token on POST request"""
    permission_classes = (IsAuthenticated,)
