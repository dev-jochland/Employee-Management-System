from dj_rest_auth.views import PasswordChangeView
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from exception import get_all_serializer_errors
import user.models as um


class CustomPasswordChangeView(PasswordChangeView):
    """This view handles a user password change request"""
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = request.user
            if um.Admin.objects.filter(user=user):
                admin = um.Admin.objects.get(user=user)
                if not admin.is_default_password_changed:
                    admin.is_default_password_changed = True
                    admin.save(update_fields=['is_default_password_changed'])
            elif um.Employee.objects.filter(user=user):
                employee = um.Employee.objects.get(user=user)
                if not employee.is_default_password_changed:
                    employee.is_default_password_changed = True
                    employee.save(update_fields=['is_default_password_changed'])
            return Response({'detail': _('New password has been saved.')}, status=status.HTTP_200_OK)
        except ValidationError as e:
            error = get_all_serializer_errors(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": _(str(e))}, status=status.HTTP_400_BAD_REQUEST)
