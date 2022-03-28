from dj_rest_auth.registration.views import RegisterView
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from exception import get_all_serializer_errors
import user.utils as ut
import user.models as um


class OnboardOrganisation(RegisterView):

    def create(self, request, *args, **kwargs):
        try:
            if message := ut.validate_required_fields(
                    {
                        'full_name': request.data.get('full_name'),
                        'password1': request.data.get('password1'),
                        'password2': request.data.get('password2'),
                        'email': request.data.get('email'),
                        'company_name': request.data.get('company_name'),
                        'role': request.data.get('role'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            if um.Organisation.objects.filter(name__iexact=request.data.get('company_name')):
                return Response({'detail': _("Company name already exists")}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            with transaction.atomic():
                user.save()
                wallet = um.Wallet.objects.create(created_by=user.id)
                # fund wallet by creating transaction history
                um.Transaction.objects.create(wallet=wallet, type='deposit', amount=999999999999999, is_verified=True,
                                              initiated_by=user.id, description='default on boarding funds')
                organisation = um.Organisation.objects.create(name=request.data.get('company_name'), created_by=user.id,
                                                              wallet=wallet, is_verified=True)
                admin = um.Admin.objects.create(user=user, created_by=user.id, is_default_password_changed=True)
                um.OrganisationAdmin.objects.create(organisation=organisation, admin=admin, admin_type='super_admin',
                                                    is_active=True, role=request.data.get('role'), created_by=user.id)
                return Response(
                    {'detail': _('Employer successfully onboarded with initial amount of nine hundred and ninety nine '
                                 'trillion (999999999999999). Please login to continue')}, status=status.HTTP_200_OK
                )
        except ValidationError as e:
            error = get_all_serializer_errors(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:  # When all possible unique wallet address permutations reached
            return Response({'detail': _('Wallet Integrity error')}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": _(str(e))}, status=status.HTTP_400_BAD_REQUEST)
