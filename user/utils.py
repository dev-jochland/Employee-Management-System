import decimal
import random
import secrets
import string

from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

import user.models as um

accepted_chars_caps = 'ABCDEFGHKLMNPQRTSUVWXYZ'
accepted_chars_low = 'abcdefghkmnpqrstuvwxyz'


def random_string_generator(size=25, chars=accepted_chars_caps + accepted_chars_low):
    return ''.join(secrets.choice(chars) for _ in range(size))


def random_wallet_number(string_digits):
    x = list(string_digits)
    random.shuffle(x)
    return str(secrets.choice(range(1000, 10000))) + "".join(x[:6])


def unique_wallet_address(instance, new_wallet_address=None):
    if new_wallet_address is not None:
        wallet_address = new_wallet_address

    else:
        wallet_address = instance.address
        Klass = instance.__class__
        if Klass.objects.filter(
                address=wallet_address
        ).exists():
            new_wallet_address = '{rand_str}-{rand_number}'.format(rand_str=random_string_generator(size=4),
                                                                   rand_number=random_wallet_number(string.digits))
            return unique_wallet_address(instance, new_wallet_address=new_wallet_address)
    return wallet_address


def validate_required_fields(fields: dict):
    return {
        'detail': f'Field {field} is required'
        for field in fields
        if not fields.get(field)
    }


def get_authenticated_email(request):
    try:
        if request.auth.get('email') is not None:  # Token User
            return request.auth.get('email')
    except AttributeError:
        return request.user.email
    except Exception as e:
        return str(e)


def set_pin_util(serializer, wallet, request, new_pin, user, is_organisation):
    if wallet.is_pin_set:
        return Response({'detail': _("Pin already set for this wallet, change wallet pin rather")},
                        status=status.HTTP_400_BAD_REQUEST)
    util_serializer = serializer(wallet, data=request.data)
    util_serializer.is_valid(raise_exception=True)
    wallet.pin = make_password(new_pin)
    wallet.is_pin_set = True
    wallet.save(update_fields=['pin', 'is_pin_set'])

    # Create Activity Log
    if is_organisation:
        um.ActivityLog.objects.create(activity_type='set_pin', wallet=wallet, created_by=user.id)
    else:
        um.ActivityLog.objects.create(activity_type='set_pin', wallet=wallet, created_by=user.id, is_organisation=False)
    return Response({'detail': _('Wallet Pin saved')}, status=status.HTTP_200_OK)


def change_pin_util(serializer, wallet, request, new_pin, old_pin, user, is_organisation):
    if not wallet.is_pin_set:
        return Response({'detail': _("Set Pin first, before changing pin")},
                        status=status.HTTP_400_BAD_REQUEST)
    change_pin_serializer = serializer(wallet, data=request.data)
    change_pin_serializer.is_valid(raise_exception=True)
    if not check_password(old_pin, encoded=wallet.pin):
        return Response({'message': "your old pin is not correct, enter a valid old pin"},
                        status=status.HTTP_400_BAD_REQUEST)
    wallet.pin = make_password(new_pin)
    wallet.save(update_fields=['pin'])

    # Create Activity Log
    if is_organisation:
        um.ActivityLog.objects.create(activity_type='changed_pin', wallet=wallet, created_by=user.id)
    else:
        um.ActivityLog.objects.create(activity_type='changed_pin', wallet=wallet, created_by=user.id,
                                      is_organisation=False)
    return Response({'detail': _('Wallet Pin updated')}, status=status.HTTP_200_OK)


def verify_wallet_pin(wallet, pin):
    if not check_password(pin, wallet.pin):
        return False
    return True


def get_wallet_balance(wallet):
    total_withdrawal = decimal.Decimal(0.0000)
    total_deposit = decimal.Decimal(0.0000)

    withdrawal = um.Transaction.objects.filter(wallet=wallet, type='withdrawal', is_verified=True)
    deposit = um.Transaction.objects.filter(wallet=wallet, type='deposit', is_verified=True)

    for _ in withdrawal:
        total_withdrawal += _.amount

    for _ in deposit:
        total_deposit += _.amount

    balance = total_deposit - total_withdrawal
    return balance


def verify_bulk_employee_data(employees, organisation):
    total_amount = 0
    if type(employees) is not list:
        return {'detail': _("Send employees in an array")}

    for employee in employees:
        if type(employee) is not dict:
            return {"detail": _('Send employee details in an object')}
        if employee.get('employee_wallet') == organisation.wallet.address:
            return {'detail': _("You can't make payment to your organisation wallet")}
        if not all(employee.values()):  # check that provided data has no none value
            return {'detail': _("Make sure all employee details are provided")}
        if employee.get('amount') is None:  # check that amount is provided in data
            return {'detail': _(f"Provide amount for for {employee.get('employee_email')}")}
        if type(employee.get('amount')) is not float:  # check that provided amount is float
            return {'detail': _(f"Provide amount in decimal for {employee.get('employee_email')}")}
        if 'e+' in str(employee.get('amount')).split('.')[0]:  # After 15 digits, float convert to scientific e
            return {'detail': _(f"Amount is too large and arbitrary for {employee.get('employee_email')}")}
        if len(str(employee.get('amount')).split('.')[1]) > 2:  # Check that amount is in two decimal places
            return {'detail': _(f"Amount should be in two decimal places for {employee.get('employee_email')}")}
        if not um.EmployeeOrganisation.objects.filter(organisation=organisation,
                                                      wallet__address=employee.get('employee_wallet'),
                                                      employee__user__email=employee.get("employee_email")):
            return {'detail': _(f"Provided employee with details: {employee.get('employee_email')} "
                                f"and {employee.get('employee_wallet')} are not correct, ensure "
                                "correct wallet address and associated email with this employee")}
        if not um.EmployeeOrganisation.objects.filter(organisation=organisation,
                                                      wallet__address=employee.get('employee_wallet'),
                                                      employee__user__email=employee.get('employee_email'),
                                                      is_active=True):
            return {'detail': _(f"Provided employee with details: {employee.get('employee_email')} "
                                f"and {employee.get('employee_wallet')} has been deactivated from your "
                                f"organisation, reactivate employee to make payments")}
        total_amount += float(employee.get('amount'))
    return total_amount


def verify_employee_data(amount, employee_wallet, employee_email, organisation):
    if type(amount) is not float:
        return {'detail': _("Provide amount in decimal")}
    if 'e+' in str(amount).split('.')[0]:  # After 15 digits, float convert to scientific e
        return {'detail': _("Amount is too large and arbitrary")}
    if len(str(amount).split('.')[1]) > 2:
        return {'detail': _("Amount should be in two decimal places")}
    if organisation.wallet.address == employee_wallet:
        return {'detail': _("You can't make payment to your organisation wallet")}
    if not um.EmployeeOrganisation.objects.filter(organisation=organisation, wallet__address=employee_wallet,
                                                  employee__user__email=employee_email):
        return {'detail': _("Provided employee details is not correct, ensure "
                            "correct wallet address and associated email with this employee")}
    if not um.EmployeeOrganisation.objects.filter(organisation=organisation, wallet__address=employee_wallet,
                                                  employee__user__email=employee_email, is_active=True):
        return {'detail': _('This employee has been deactivated from your organisation, reactivate '
                            'employee to make payments')}
    return amount

