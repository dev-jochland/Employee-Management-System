from django.contrib import admin
import user.models as um


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name')
    search_fields = ('email',)


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_verified', 'wallet', 'is_deleted', 'date_created')
    search_fields = ('name',)
    list_filter = ('is_deleted', 'is_verified')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_of_birth', 'is_default_password_changed', 'is_deleted', 'date_created')
    search_fields = ('user',)
    list_filter = ('is_deleted', )


class EmployeeOrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'organisation', 'wallet', 'is_active', 'date_created')
    search_fields = ('employee', 'organisation')
    list_filter = ('is_deleted', 'is_active')


class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_default_password_changed', 'is_deleted', 'date_created')
    search_fields = ('user',)
    list_filter = ('is_deleted', )


class OrganisationAdminModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'organisation', 'admin', 'admin_type', 'is_active', 'is_disabled', 'role', 'is_deleted',
                    'date_created')
    search_fields = ('organisation', 'admin')
    list_filter = ('is_deleted', 'is_active', 'is_disabled', 'admin_type')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'transaction_id', 'type', 'amount', 'initiator_wallet', 'is_verified',
                    'initiated_by', 'date_created')
    list_filter = ('is_deleted', 'type')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'pin', 'is_pin_set', 'date_created')
    search_fields = ('address',)
    list_filter = ('is_deleted', 'is_pin_set')


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'activity_type', 'wallet', 'user_affected', 'created_by', 'is_organisation')
    list_filter = ("is_organisation", )


admin.site.register(um.AppUser, UserAdmin)
admin.site.register(um.Organisation, OrganisationAdmin)
admin.site.register(um.Employee, EmployeeAdmin)
admin.site.register(um.EmployeeOrganisation, EmployeeOrganisationAdmin)
admin.site.register(um.Admin, AdminModelAdmin)
admin.site.register(um.OrganisationAdmin, OrganisationAdminModelAdmin)
admin.site.register(um.Transaction, TransactionAdmin)
admin.site.register(um.Wallet, WalletAdmin)
admin.site.register(um.ActivityLog, ActivityLogAdmin)
