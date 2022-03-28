from rest_framework.permissions import AllowAny, BasePermission

import user.models as um
import user.utils as ut


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """

    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
            elif view.action is None:
                return True  # This handles 'OPTIONS' HTTP methods
        return False


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.auth is None:
            return False
        email = ut.get_authenticated_email(request)
        super_admin = um.OrganisationAdmin.objects.filter(admin__user__email=email, admin_type='super_admin',
                                                          is_deleted=False, is_active=True, is_disabled=False)
        return bool(super_admin)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.auth is None:
            return False
        email = ut.get_authenticated_email(request)
        admin = um.OrganisationAdmin.objects.filter(admin__user__email=email, admin_type='admin', is_deleted=False,
                                                    is_active=True, is_disabled=False)
        return bool(admin)


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        if request.auth is None:
            return False
        email = ut.get_authenticated_email(request)
        employee = um.EmployeeOrganisation.objects.filter(employee__user__email=email, is_deleted=False)
        return bool(employee)


