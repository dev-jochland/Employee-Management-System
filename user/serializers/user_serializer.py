import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import user.models as um
import user.utils as ut

UserModel = get_user_model()


class JWTUserDetailSerializer(serializers.ModelSerializer):
    """This serializer handles the returned data on user login along with the jwt tokens in postman"""

    class Meta:
        model = UserModel
        fields = ('id',)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extra payload data saved in my token key for use with request.auth"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token


class OrganisationDashboardSerializer(serializers.ModelSerializer):
    number_of_employees = serializers.SerializerMethodField()
    active_employees = serializers.SerializerMethodField()
    wallet = serializers.ReadOnlyField(source='wallet.address')
    is_default_password_changed = serializers.SerializerMethodField()
    number_of_inactive_employees = serializers.SerializerMethodField()
    number_of_active_employees = serializers.SerializerMethodField()
    inactive_employees = serializers.SerializerMethodField()
    wallet_balance = serializers.SerializerMethodField()

    class Meta:
        model = um.Organisation
        fields = ('id', 'name', 'wallet', 'wallet_balance',  'profile', 'is_default_password_changed',
                  'number_of_employees', 'number_of_active_employees', 'number_of_inactive_employees',
                  'active_employees', 'inactive_employees')

    @staticmethod
    def get_number_of_employees(obj):
        return um.EmployeeOrganisation.objects.filter(organisation=obj, is_deleted=False).count()

    @staticmethod
    def get_number_of_inactive_employees(obj):
        return um.EmployeeOrganisation.objects.filter(organisation=obj, is_active=False, is_deleted=False).count()

    @staticmethod
    def get_number_of_active_employees(obj):
        return um.EmployeeOrganisation.objects.filter(organisation=obj, is_active=True, is_deleted=False).count()

    @staticmethod
    def get_active_employees(obj):
        employee_organisation = um.EmployeeOrganisation.objects.filter(organisation=obj, is_active=True,
                                                                       is_deleted=False)
        serializer = OrganisationEmployeeOrganisationSerializer(employee_organisation, many=True)
        return serializer.data

    @staticmethod
    def get_inactive_employees(obj):
        employee_organisation = um.EmployeeOrganisation.objects.filter(organisation=obj, is_active=False,
                                                                       is_deleted=False)
        serializer = OrganisationEmployeeOrganisationSerializer(employee_organisation, many=True)
        return serializer.data

    def get_is_default_password_changed(self, obj):
        admin = self.context.get('admin')
        return admin.is_default_password_changed

    @staticmethod
    def get_wallet_balance(obj):
        return ut.get_wallet_balance(obj.wallet)


class EmployeeOrganisationSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='employee.user.email')
    wallet = serializers.ReadOnlyField(source='wallet.address')
    employee = serializers.ReadOnlyField(source='employee.user.full_name')
    organisation = serializers.ReadOnlyField(source='organisation.name')
    organisation_id = serializers.ReadOnlyField(source='organisation.id')
    wallet_balance = serializers.SerializerMethodField()

    class Meta:
        model = um.EmployeeOrganisation
        fields = ('organisation_id', 'employee', 'email', 'wallet', "wallet_balance", 'is_active', 'organisation')

    @staticmethod
    def get_wallet_balance(obj):
        return ut.get_wallet_balance(obj.wallet)


class OrganisationEmployeeOrganisationSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='employee.user.email')
    wallet = serializers.ReadOnlyField(source='wallet.address')
    employee = serializers.ReadOnlyField(source='employee.user.full_name')
    organisation = serializers.ReadOnlyField(source='organisation.name')
    organisation_id = serializers.ReadOnlyField(source='organisation.id')

    class Meta:
        model = um.EmployeeOrganisation
        fields = ('organisation_id', 'employee', 'email', 'wallet', 'is_active', 'organisation')


class EmployeeDashboardSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user.full_name')
    active_organisations = serializers.SerializerMethodField()
    number_of_organisation = serializers.SerializerMethodField()
    number_of_active_organisation = serializers.SerializerMethodField()
    number_of_inactive_organisation = serializers.SerializerMethodField()
    inactive_organisations = serializers.SerializerMethodField()

    class Meta:
        model = um.Employee
        fields = ('id', 'name', 'image', 'date_of_birth', 'is_default_password_changed', 'number_of_organisation',
                  'number_of_active_organisation', 'number_of_inactive_organisation', 'active_organisations',
                  'inactive_organisations')

    @staticmethod
    def get_number_of_organisation(obj):
        return um.EmployeeOrganisation.objects.filter(employee=obj, is_deleted=False).count()

    @staticmethod
    def get_number_of_active_organisation(obj):
        return um.EmployeeOrganisation.objects.filter(employee=obj, is_deleted=False, is_active=True).count()

    @staticmethod
    def get_number_of_inactive_organisation(obj):
        return um.EmployeeOrganisation.objects.filter(employee=obj, is_deleted=False, is_active=False).count()

    @staticmethod
    def get_active_organisations(obj):
        employee_organisation = um.EmployeeOrganisation.objects.filter(employee=obj, is_deleted=False, is_active=True)
        serializer = EmployeeOrganisationSerializer(employee_organisation, many=True)
        return serializer.data

    @staticmethod
    def get_inactive_organisations(obj):
        employee_organisation = um.EmployeeOrganisation.objects.filter(employee=obj, is_deleted=False, is_active=False)
        serializer = EmployeeOrganisationSerializer(employee_organisation, many=True)
        return serializer.data


class WalletPinSerializer(serializers.Serializer):
    new_pin = serializers.CharField(
        required=True,
        validators=[MinLengthValidator(6)],
        max_length=6
    )
    confirm_new_pin = serializers.CharField(
        required=True,
        validators=[MinLengthValidator(6)],
        max_length=6
    )

    def validate(self, data):
        if data.get('new_pin') != data.get('confirm_new_pin'):
            raise serializers.ValidationError(_('Error! Make sure your new_pin and confirm_pin are the same'))
        return data


class OrganisationAdminSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='admin.user.full_name')
    email = serializers.ReadOnlyField(source='admin.user.email')

    class Meta:
        model = um.OrganisationAdmin
        fields = ("name", "is_disabled", 'role', 'email', 'organisation')


class UpdateOrganisationSerializer(serializers.ModelSerializer):
    wallet = serializers.ReadOnlyField(source='wallet.address')

    class Meta:
        model = um.Organisation
        fields = ('id', 'name', 'profile', 'is_verified', 'wallet')
        read_only_fields = ('id', 'name', 'is_verified', 'wallet')


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='user.full_name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = um.Employee
        fields = ('id', 'full_name', 'email', 'date_of_birth', 'image')

    def validate_date_of_birth(self, value_of_date):
        today = datetime.date.today()
        age = relativedelta(today, value_of_date)
        if age.years < 16:
            raise serializers.ValidationError(_("You must be 16 years and above"))

        return value_of_date

