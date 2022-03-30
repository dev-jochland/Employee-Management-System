import re

from django.db import transaction, IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import user.serializers.user_serializer as usu
from exception import get_all_serializer_errors
import permissions as pp
import user.utils as ut
import user.models as um
import user.tasks as task

valid_email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class EmployerViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[pp.IsAdmin | pp.IsSuperAdmin])
    def add_employee(self, request):
        try:
            if message := ut.validate_required_fields(
                    {
                        'full_name': request.data.get('full_name'),
                        'email': request.data.get('email'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            full_name = request.data.get('full_name')
            if len(full_name.split(' ')) < 2 or len(full_name.split(' ')[1]) < 1:
                return Response({'detail': _('Provide employee full name')}, status=status.HTTP_400_BAD_REQUEST)
            if not re.fullmatch(valid_email_regex, request.data.get('email')):
                return Response({'detail': _("Invalid email format")}, status=status.HTTP_400_BAD_REQUEST)
            if um.Admin.objects.filter(user__email__iexact=request.data.get('email')):
                return Response({'detail': _("Cannot add admin user")}, status=status.HTTP_400_BAD_REQUEST)
            admin_email = ut.get_authenticated_email(request)
            admin_user = um.AppUser.objects.get(email=admin_email)
            admin_organisation = um.OrganisationAdmin.objects.get(admin__user__email=admin_email).organisation
            if um.Employee.objects.filter(user__email__iexact=request.data.get('email'), is_deleted=False):
                employee = um.Employee.objects.get(user__email__iexact=request.data.get('email'))
                if um.EmployeeOrganisation.objects.filter(organisation=admin_organisation, employee=employee,
                                                          is_active=True, is_deleted=False):
                    return Response({'detail': _('User is already an employee in your organisation')},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif um.EmployeeOrganisation.objects.filter(organisation=admin_organisation, employee=employee,
                                                            is_active=False, is_deleted=False):
                    return Response({'detail': _('Employee is inactive in your organisation, reactivate employee '
                                                 'instead')}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    wallet = um.Wallet.objects.create(created_by=employee.user.id)
                    um.EmployeeOrganisation.objects.create(employee=employee, organisation=admin_organisation,
                                                           wallet=wallet, created_by=employee.user.id)
                    um.ActivityLog.objects.create(activity_type='add_employee', created_by=admin_user.id,
                                                  is_organisation=True, user_affected=employee.user)
                    return Response({'detail': 'Employee added successfully.'},
                                    status=status.HTTP_200_OK)
            else:
                with transaction.atomic():
                    user = um.AppUser.objects.create_user(email=request.data.get('email'), password='testpassword',
                                                          full_name=request.data.get('full_name'))
                    wallet = um.Wallet.objects.create(created_by=user.id)
                    employee = um.Employee.objects.create(user=user, created_by=user.id)
                    um.EmployeeOrganisation.objects.create(employee=employee, organisation=admin_organisation,
                                                           wallet=wallet, created_by=user.id)
                    um.ActivityLog.objects.create(activity_type='add_employee', created_by=admin_user.id,
                                                  is_organisation=True, user_affected=user)
                    return Response({'detail': 'Employee added successfully with default password: testpassword'},
                                    status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({'detail': _('Wallet Integrity Error')}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[pp.IsAdmin | pp.IsSuperAdmin])
    def dashboard(self, request):
        try:
            email = ut.get_authenticated_email(request)
            organisation = um.OrganisationAdmin.objects.get(admin__user__email=email).organisation
            admin = um.Admin.objects.get(user__email=email)
            serializer = usu.OrganisationDashboardSerializer(organisation, context={'admin': admin})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[pp.IsSuperAdmin])
    def add_admin(self, request):
        try:
            if message := ut.validate_required_fields(
                    {
                        'full_name': request.data.get('full_name'),
                        'email': request.data.get('email'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            full_name = request.data.get('full_name')
            if len(full_name.split(' ')) < 2 or len(full_name.split(' ')[1]) < 1:
                return Response({'detail': _('Provide admin full name')}, status=status.HTTP_400_BAD_REQUEST)
            if not re.fullmatch(valid_email_regex, request.data.get('email')):
                return Response({'detail': _("Invalid email format")}, status=status.HTTP_400_BAD_REQUEST)
            if um.AppUser.objects.filter(email__iexact=request.data.get('email')):
                return Response({'detail': _("This email is already registered on the platform")},
                                status=status.HTTP_400_BAD_REQUEST)
            super_admin_email = ut.get_authenticated_email(request)
            super_admin_user = um.AppUser.objects.get(email=super_admin_email)
            super_admin_organisation = um.OrganisationAdmin.objects.get(
                admin__user__email=super_admin_email).organisation
            with transaction.atomic():
                user = um.AppUser.objects.create_user(email=request.data.get('email'), password='testpassword',
                                                      full_name=request.data.get('full_name'))
                admin = um.Admin.objects.create(user=user, created_by=user.id)
                um.OrganisationAdmin.objects.create(organisation=super_admin_organisation, admin=admin,
                                                    admin_type='admin', is_active=True, created_by=super_admin_user.id)
                um.ActivityLog.objects.create(activity_type='add_admin', created_by=super_admin_user.id,
                                              is_organisation=True, user_affected=user)
            return Response({'detail': _('Admin added successfully with default password: testpassword')},
                            status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({'detail': _('Wallet Integrity Error')}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], permission_classes=[pp.IsAdmin | pp.IsSuperAdmin])
    def remove_employee(self, request):
        try:
            employee_email = request.data.get('employee_email')
            if message := ut.validate_required_fields(
                    {
                        'employee_email': request.data.get('employee_email'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            admin_email = ut.get_authenticated_email(request)
            admin_user = um.AppUser.objects.get(email=admin_email)
            admin_organisation = um.OrganisationAdmin.objects.get(admin__user=admin_user).organisation
            if not um.EmployeeOrganisation.objects.filter(organisation=admin_organisation,
                                                          employee__user__email=employee_email):
                return Response({'detail': _('This employee is not part of this organisation')},
                                status=status.HTTP_400_BAD_REQUEST)
            if um.EmployeeOrganisation.objects.filter(organisation=admin_organisation,
                                                      employee__user__email=employee_email, is_active=False):
                return Response({'detail': _("Employee is already deactivated from organisation")},
                                status=status.HTTP_400_BAD_REQUEST)
            employee = um.EmployeeOrganisation.objects.get(organisation=admin_organisation,
                                                           employee__user__email=employee_email, is_active=True)
            employee.is_active = False
            employee.save(update_fields=['is_active'])

            # Create Organisation Activity Log
            um.ActivityLog.objects.create(activity_type='remove_employee', created_by=admin_user.id,
                                          user_affected=employee.employee.user, is_organisation=True)
            return Response({'detail': _("Employee deactivated from organisation successfully")},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], permission_classes=[pp.IsAdmin | pp.IsSuperAdmin])
    def reactivate_employee(self, request):
        try:
            employee_email = request.data.get('employee_email')
            if message := ut.validate_required_fields(
                    {
                        'employee_email': request.data.get('employee_email'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            admin_email = ut.get_authenticated_email(request)
            admin_user = um.AppUser.objects.get(email=admin_email)
            admin_organisation = um.OrganisationAdmin.objects.get(admin__user=admin_user).organisation
            if not um.EmployeeOrganisation.objects.filter(organisation=admin_organisation,
                                                          employee__user__email=employee_email):
                return Response({'detail': _('This employee is not part of this organisation')},
                                status=status.HTTP_400_BAD_REQUEST)
            if um.EmployeeOrganisation.objects.filter(organisation=admin_organisation,
                                                      employee__user__email=employee_email, is_active=True):
                return Response({'detail': _("Employee is already active in your organisation")},
                                status=status.HTTP_400_BAD_REQUEST)
            employee = um.EmployeeOrganisation.objects.get(organisation=admin_organisation,
                                                           employee__user__email=employee_email, is_active=False)
            employee.is_active = True
            employee.save(update_fields=['is_active'])

            # Create Organisation Activity Log
            um.ActivityLog.objects.create(activity_type='re_activated_employee', created_by=admin_user.id,
                                          user_affected=employee.employee.user, is_organisation=True)
            return Response({'detail': _("Employee reactivated to organisation successfully")},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], permission_classes=[pp.IsSuperAdmin])
    def remove_admin(self, request):
        try:
            admin_email = request.data.get('admin_email')
            if message := ut.validate_required_fields(
                    {
                        'admin_email': request.data.get('admin_email'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            super_admin_email = ut.get_authenticated_email(request)
            super_admin_user = um.AppUser.objects.get(email=super_admin_email)
            admin_organisation = um.OrganisationAdmin.objects.get(admin__user=super_admin_user).organisation
            if super_admin_email == admin_email.lower():
                return Response({'detail': _("Super admin can\'t remove itself, contact product administrator.")},
                                status=status.HTTP_400_BAD_REQUEST)
            if not um.OrganisationAdmin.objects.filter(organisation=admin_organisation,
                                                       admin__user__email=admin_email):
                return Response({'detail': _('This admin is not part of this organisation')},
                                status=status.HTTP_400_BAD_REQUEST)
            if um.OrganisationAdmin.objects.filter(organisation=admin_organisation,
                                                   admin__user__email=admin_email, is_disabled=True):
                return Response({'detail': _("Admin already removed from organisation")},
                                status=status.HTTP_400_BAD_REQUEST)
            admin = um.OrganisationAdmin.objects.get(organisation=admin_organisation,
                                                     admin__user__email=admin_email, is_disabled=False)
            admin.is_disabled = True
            admin.save(update_fields=['is_disabled'])

            # Create Organisation Activity Log
            um.ActivityLog.objects.create(activity_type='remove_admin', created_by=super_admin_user.id,
                                          user_affected=admin.admin.user, is_organisation=True)
            return Response({'detail': _("Admin removed from organisation successfully")},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[pp.IsSuperAdmin], url_path='admins', url_name='admins')
    def get_all_admins(self, request):
        try:
            email = ut.get_authenticated_email(request)
            super_admin_organisation = um.OrganisationAdmin.objects.get(admin__user__email=email,
                                                                        admin_type='super_admin').organisation
            organisation_admins = um.OrganisationAdmin.objects.filter(organisation=super_admin_organisation,
                                                                      admin_type='admin')
            serializer = usu.OrganisationAdminSerializer(organisation_admins, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[pp.IsSuperAdmin | pp.IsAdmin], url_path='profile',
            url_name='profile')
    def update_profile(self, request, pk=None):
        try:
            organisation_id = self.kwargs.get('pk')
            if not um.Organisation.objects.filter(id=organisation_id, is_deleted=False):
                return Response({'detail': _("Organisation does not exist")}, status=status.HTTP_400_BAD_REQUEST)
            email = ut.get_authenticated_email(request)
            if not um.OrganisationAdmin.objects.filter(organisation_id=organisation_id, admin__user__email=email):
                return Response({'detail': _('You don not have access to this organisation')},
                                status=status.HTTP_403_FORBIDDEN)
            organisation = um.Organisation.objects.get(id=organisation_id)
            serializer = usu.UpdateOrganisationSerializer(organisation, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            error = get_all_serializer_errors(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[pp.IsSuperAdmin | pp.IsAdmin])
    def pay_employee(self, request):
        try:
            if message := ut.validate_required_fields(
                    {
                        'employee_wallet': request.data.get('employee_wallet'),
                        'employee_email': request.data.get('employee_email'),
                        "amount": request.data.get('amount'),
                        "pin": request.data.get('pin'),
                        'description': request.data.get('description'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            email = ut.get_authenticated_email(request)
            admin_user = um.AppUser.objects.get(email=email)
            organisation = um.OrganisationAdmin.objects.get(admin__user=admin_user).organisation

            # sanitise employee data
            verify_employee_data = ut.verify_employee_data(request.data.get('amount'),
                                                           request.data.get('employee_wallet'),
                                                           request.data.get('employee_email'), organisation)
            if type(verify_employee_data) is dict:
                return Response(verify_employee_data, status=status.HTTP_400_BAD_REQUEST)

            if organisation.wallet.pin is None:
                return Response({'detail': 'Set wallet pin before making payment'}, status=status.HTTP_400_BAD_REQUEST)

            verify_pin = ut.verify_wallet_pin(organisation.wallet, str(request.data.get('pin')))
            if not verify_pin:
                return Response({'detail': _('Incorrect wallet pin provided')}, status=status.HTTP_400_BAD_REQUEST)

            balance = ut.get_wallet_balance(organisation.wallet)
            cleaned_amount = verify_employee_data
            if cleaned_amount > balance:
                return Response({'detail': _('Insufficient funds in wallet')}, status=status.HTTP_400_BAD_REQUEST)

            # Push payment to celery queue
            task.make_employee_payment.delay(request.data.get('employee_wallet'), request.data.get('description'),
                                             admin_user, organisation, cleaned_amount)

            return Response({'detail': _("Payment successfully made to employee")}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[pp.IsSuperAdmin | pp.IsAdmin])
    def bulk_pay_employees(self, request):
        try:
            if message := ut.validate_required_fields(
                    {
                        "employees": request.data.get('employees'),
                        "pin": request.data.get('pin'),
                        'description': request.data.get('description'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            email = ut.get_authenticated_email(request)
            admin_user = um.AppUser.objects.get(email=email)
            organisation = um.OrganisationAdmin.objects.get(admin__user=admin_user).organisation

            # Sanitise provided data
            verify_data = ut.verify_bulk_employee_data(request.data.get('employees'), organisation)
            if type(verify_data) is dict:
                return Response(verify_data, status=status.HTTP_400_BAD_REQUEST)

            if organisation.wallet.pin is None:
                return Response({'detail': 'Set wallet pin before making payment'}, status=status.HTTP_400_BAD_REQUEST)

            verify_pin = ut.verify_wallet_pin(organisation.wallet, str(request.data.get('pin')))
            if not verify_pin:
                return Response({'detail': _('Incorrect wallet pin provided')}, status=status.HTTP_400_BAD_REQUEST)

            balance = ut.get_wallet_balance(organisation.wallet)
            cleaned_total_amount = verify_data
            if cleaned_total_amount > balance:
                return Response({'detail': _('Insufficient funds in wallet')}, status=status.HTTP_400_BAD_REQUEST)

            # push payment to celery queue
            task.make_bulk_payment.delay(request.data.get('employees'), request.data.get('description'), admin_user,
                                         organisation)
            return Response({'detail': "Bulk payment made successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WalletViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['patch'], permission_classes=[pp.IsSuperAdmin | pp.IsEmployee])
    def set_pin(self, request):
        try:
            if message := ut.validate_required_fields(
                    {
                        'organisation_id': request.data.get('organisation_id'),
                        'wallet_address': request.data.get('wallet_address'),
                        'new_pin': request.data.get('new_pin'),
                        'confirm_new_pin': request.data.get('confirm_new_pin'),
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            organisation_id = request.data.get('organisation_id')
            wallet_address = request.data.get('wallet_address')
            new_pin = request.data.get('new_pin')
            confirm_new_pin = request.data.get('confirm_new_pin')
            if not str(new_pin).isdigit():
                return Response({'detail': _("New Pin must be numbers only")}, status=status.HTTP_400_BAD_REQUEST)
            if not str(confirm_new_pin).isdigit():
                return Response({'detail': _("Confirm New Pin must be numbers only")},
                                status=status.HTTP_400_BAD_REQUEST)
            email = ut.get_authenticated_email(request)
            user = um.AppUser.objects.get(email=email)
            if um.Admin.objects.filter(user__email=email):
                if not um.OrganisationAdmin.objects.filter(organisation_id=organisation_id, admin__user__email=email):
                    return Response({'detail': _('You do not have access to this organisation')},
                                    status=status.HTTP_403_FORBIDDEN)
                wallet = um.Organisation.objects.get(id=organisation_id, wallet__address=wallet_address,
                                                     is_deleted=False).wallet
                setup_pin = ut.set_pin_util(usu.WalletPinSerializer, wallet, request, new_pin, user, True)
                return Response(setup_pin.data, status=setup_pin.status_code)
            elif um.EmployeeOrganisation.objects.filter(organisation_id=organisation_id, employee__user__email=email):
                wallet = um.EmployeeOrganisation.objects.get(organisation_id=organisation_id,
                                                             employee__user__email=email,
                                                             wallet__address=wallet_address).wallet
                setup_pin = ut.set_pin_util(usu.WalletPinSerializer, wallet, request, new_pin, user, False)
                return Response(setup_pin.data, status=setup_pin.status_code)
            return Response({'detail': _('Invalid user')}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            error = get_all_serializer_errors(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except um.Organisation.DoesNotExist:
            return Response({'detail': _('Your organisation does not have access to this wallet')},
                            status=status.HTTP_400_BAD_REQUEST)
        except um.EmployeeOrganisation.DoesNotExist:
            return Response({'detail': _('You are not the owner of this wallet or the wallet is not tied to the '
                                         'provided employee organisation')}, status=status.HTTP_400_BAD_REQUEST)
        except um.AppUser.DoesNotExist:
            return Response({'detail': _('User does not exist')}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], permission_classes=[pp.IsSuperAdmin | pp.IsEmployee])
    def change_pin(self, request):
        try:
            if message := ut.validate_required_fields(
                    {
                        'organisation_id': request.data.get('organisation_id'),
                        'wallet_address': request.data.get('wallet_address'),
                        'new_pin': request.data.get('new_pin'),
                        'confirm_new_pin': request.data.get('confirm_new_pin'),
                        'old_pin': request.data.get('old_pin')
                    }
            ):
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            organisation_id = request.data.get('organisation_id')
            wallet_address = request.data.get('wallet_address')
            new_pin = request.data.get('new_pin')
            confirm_new_pin = request.data.get('confirm_new_pin')
            old_pin = request.data.get('old_pin')
            if not str(new_pin).isdigit():
                return Response({'detail': _("New Pin must be numbers only")}, status=status.HTTP_400_BAD_REQUEST)
            if not str(confirm_new_pin).isdigit():
                return Response({'detail': _("Confirm New Pin must be numbers only")},
                                status=status.HTTP_400_BAD_REQUEST)
            email = ut.get_authenticated_email(request)
            user = um.AppUser.objects.get(email=email)
            if um.Admin.objects.filter(user__email=email):
                if not um.OrganisationAdmin.objects.filter(organisation_id=organisation_id, admin__user__email=email):
                    return Response({'detail': _('You do not have access to this organisation')},
                                    status=status.HTTP_403_FORBIDDEN)
                wallet = um.Organisation.objects.get(id=organisation_id, wallet__address=wallet_address,
                                                     is_deleted=False).wallet
                change_pin = ut.change_pin_util(usu.WalletPinSerializer, wallet, request, new_pin, old_pin, user, True)
                return Response(change_pin.data, status=change_pin.status_code)
            elif um.EmployeeOrganisation.objects.filter(organisation_id=organisation_id, employee__user__email=email):
                wallet = um.EmployeeOrganisation.objects.get(organisation_id=organisation_id,
                                                             employee__user__email=email,
                                                             wallet__address=wallet_address).wallet
                change_pin = ut.change_pin_util(usu.WalletPinSerializer, wallet, request, new_pin, old_pin, user, False)
                return Response(change_pin.data, status=change_pin.status_code)
            # for when an employee provides invalid organisation id
            return Response({'detail': _('You are not part of this organisation')}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            error = get_all_serializer_errors(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except um.Organisation.DoesNotExist:
            return Response({'detail': _('Your organisation does not have access to this wallet')},
                            status=status.HTTP_400_BAD_REQUEST)
        except um.EmployeeOrganisation.DoesNotExist:
            return Response({'detail': _('You are not the owner of this wallet or the wallet is not tied to the '
                                         'provided employee organisation')}, status=status.HTTP_400_BAD_REQUEST)
        except um.AppUser.DoesNotExist:
            return Response({'detail': _('User does not exist')}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeViewSet(viewsets.ModelViewSet):
    @action(detail=False, permission_classes=[pp.IsEmployee])
    def dashboard(self, request):
        try:
            email = ut.get_authenticated_email(request)
            employee = um.Employee.objects.get(user__email=email)
            serializer = usu.EmployeeDashboardSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[pp.IsEmployee], url_path='profile', url_name='profile')
    def update_profile(self, request, pk=None):
        try:
            employee_id = self.kwargs.get('pk')
            if not um.Employee.objects.filter(id=employee_id, is_deleted=False):
                return Response({'detail': _('Employee does not exist')}, status=status.HTTP_400_BAD_REQUEST)
            email = ut.get_authenticated_email(request)
            if not um.Employee.objects.filter(user__email=email, id=employee_id):
                return Response({'detail': "You can't make update for this employee"}, status=status.HTTP_403_FORBIDDEN)
            employee = um.Employee.objects.get(id=employee_id)
            full_name = request.data.get('full_name')
            if full_name is not None:
                if len(full_name.split(' ')) < 2 or len(full_name.split(' ')[1]) < 1:
                    return Response({'detail': _('Provide employee full name')}, status=status.HTTP_400_BAD_REQUEST)
            serializer = usu.EmployeeSerializer(employee, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if full_name is not None:
                employee.user.full_name = full_name
                employee.user.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            error = get_all_serializer_errors(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': _(str(e))}, status=status.HTTP_400_BAD_REQUEST)
