import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver

from parent_model import TableMetaData
from user.managers import CustomUserManager
from user.utils import unique_wallet_address


class AppUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, validators=[validate_email])
    full_name = models.CharField(max_length=250)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.full_name


class Organisation(TableMetaData):
    name = models.CharField(max_length=250, unique=True)
    profile = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # For when organisation need to be verified before performing some
    # actions
    wallet = models.OneToOneField('Wallet', on_delete=models.SET_NULL, related_name='organisation', null=True)

    def __str__(self):
        return self.name


class Employee(TableMetaData):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='employee')
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.TextField(default='', blank=True)
    is_default_password_changed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.__str__()


class EmployeeOrganisation(TableMetaData):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_organisation')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='employee_org')
    wallet = models.ForeignKey('Wallet', on_delete=models.SET_NULL, related_name='employee_wallet', null=True)
    is_active = models.BooleanField(default=True)  # Allow organisation to remove employee from organisation

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'organisation'],
                                    condition=Q(is_deleted=False),
                                    name='unique_employee_organisation')
        ]

    def __str__(self):
        return self.employee.__str__()


class Admin(TableMetaData):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='admin')
    is_default_password_changed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


ADMIN_TYPE = (
    ("super_admin", "Super Admin"),
    ("admin", "Admin"),
)


class OrganisationAdmin(TableMetaData):
    """Should a time comes when an admin can belong to different companies"""
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='organisation_admin')
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='company_admin')
    admin_type = models.CharField(choices=ADMIN_TYPE, max_length=45)
    is_active = models.BooleanField(default=False)  # True, when admin accept invite, not applicable to super_admin
    is_disabled = models.BooleanField(default=False)  # Allow company to disable admin access to company and platform
    role = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['admin', 'organisation'],
                                    condition=Q(is_deleted=False),
                                    name='unique_admin_organisation')
        ]

    def __str__(self):
        return self.organisation.name + ' ' + self.admin.user.full_name


TRANSACTION_TYPE = (
    ('deposit', 'Deposit'),
    ('withdrawal', 'Withdrawal')
)


class Transaction(TableMetaData):
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, related_name='transaction_history', editable=False)
    type = models.CharField(choices=TRANSACTION_TYPE, max_length=50, editable=False)
    amount = models.DecimalField(max_digits=19, decimal_places=4, editable=False)
    transaction_id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    is_verified = models.BooleanField(default=False, editable=False)
    initiated_by = models.CharField(max_length=250, editable=False)  # save user id here
    initiator_wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, related_name='transaction_reference',
                                         null=True, blank=True, editable=False)  # Null is true only at on boarding
    # company, when funding wallet with default funds
    initiator_is_business = models.BooleanField(default=True, editable=False)
    description = models.CharField(max_length=250, null=True, blank=True)

    def str(self):
        return self.wallet


class Wallet(TableMetaData):
    address = models.CharField(max_length=50, unique=True, editable=False)
    pin = models.CharField(null=True, blank=True, max_length=128, editable=False)
    is_pin_set = models.BooleanField(default=False)

    def __str__(self):
        return self.address


@receiver(pre_save, sender=Wallet)
def generate_wallet_address(sender, instance, *args, **kwargs):
    instance.address = unique_wallet_address(instance)


ACTIVITY_TYPE = (
    ('changed_pin', 'Changed PIN'),
    ('add_employee', 'Added Employee'),
    ('add_admin', 'Added Admin'),
    ('remove_employee', 'Removed Employee'),
    ('remove_admin', 'Removed Admin'),
    ('re_activated_employee', 'ReActivated Employee'),
    ('set_pin', 'Set Pin')
)


class ActivityLog(TableMetaData):
    activity_type = models.CharField(choices=ACTIVITY_TYPE, max_length=55)
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, related_name='activity_log_wallet')
    # Change pin or set pin does not involve user, that's why user is null below
    user_affected = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='activity_log', null=True)
    is_organisation = models.BooleanField(default=True)  # Organisation would be generating most of the activity

    def __str__(self):
        return self.activity_type
