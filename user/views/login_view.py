from dj_rest_auth.views import LoginView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from exception import get_all_serializer_errors
import user.models as um
import user.utils as ut


class OrganisationLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        try:
            self.request = request
            if message := ut.validate_required_fields(
                    {
                        'password': request.data.get('password'),
                        'email': request.data.get('email'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            if not um.Admin.objects.filter(user__email__iexact=request.data.get('email')):
                return Response({'detail': _('You are not an admin')}, status=status.HTTP_400_BAD_REQUEST)
            self.serializer = self.get_serializer(data=self.request.data)
            self.serializer.is_valid(raise_exception=True)
            self.login()
            return self.get_response()
        except ValidationError as e:
            error = get_all_serializer_errors(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": _(str(e))}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        try:
            self.request = request
            if message := ut.validate_required_fields(
                    {
                        'password': request.data.get('password'),
                        'email': request.data.get('email'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            if not um.Employee.objects.filter(user__email__iexact=request.data.get('email')):
                return Response({'detail': _('You are not an employee')}, status=status.HTTP_400_BAD_REQUEST)
            self.serializer = self.get_serializer(data=self.request.data)
            self.serializer.is_valid(raise_exception=True)
            self.login()
            return self.get_response()
        except ValidationError as e:
            error = get_all_serializer_errors(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": _(str(e))}, status=status.HTTP_400_BAD_REQUEST)
