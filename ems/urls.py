from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from user.views import login_view as lv
from user.views import register_view as rv
from user.views import password_change_view as pcv
from user.views import logout_view as lgv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),

    re_path(r'^api/auth/logout/$', lgv.CustomLogoutView.as_view(), name='rest_logout'),
    re_path(r'^api/auth/organisation/signup/$', rv.OnboardOrganisation.as_view(), name='rest_register'),
    re_path(r'^api/auth/change_password/$', pcv.CustomPasswordChangeView.as_view(), name='rest_password_change'),
    re_path(r'^api/auth/organisation/login/$', lv.OrganisationLoginView.as_view(), name='rest_login'),
    re_path(r'^api/auth/individual/login/$', lv.EmployeeLoginView.as_view(), name='rest_login2'),
    re_path(r'^api/auth/token-verify/$', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^api/auth/token-refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
