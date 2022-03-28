# Generated by Django 4.0.3 on 2022-03-28 15:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import user.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('full_name', models.CharField(max_length=250)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', user.managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_by', models.CharField(blank=True, max_length=150, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('is_default_password_changed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_by', models.CharField(blank=True, max_length=150, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('image', models.TextField(blank=True, default='')),
                ('is_default_password_changed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_by', models.CharField(blank=True, max_length=150, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('profile', models.TextField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_by', models.CharField(blank=True, max_length=150, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('address', models.CharField(editable=False, max_length=50, unique=True)),
                ('pin', models.CharField(blank=True, editable=False, max_length=128, null=True)),
                ('is_pin_set', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('created_by', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_by', models.CharField(blank=True, max_length=150, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('type', models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], editable=False, max_length=50)),
                ('amount', models.DecimalField(decimal_places=4, editable=False, max_digits=19)),
                ('transaction_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_verified', models.BooleanField(default=False, editable=False)),
                ('initiated_by', models.CharField(editable=False, max_length=250)),
                ('initiator_is_business', models.BooleanField(default=True, editable=False)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('initiator_wallet', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_reference', to='user.wallet')),
                ('wallet', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_history', to='user.wallet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganisationAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_by', models.CharField(blank=True, max_length=150, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('admin_type', models.CharField(choices=[('super_admin', 'Super Admin'), ('admin', 'Admin')], max_length=45)),
                ('is_active', models.BooleanField(default=False)),
                ('is_disabled', models.BooleanField(default=False)),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_admin', to='user.admin')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organisation_admin', to='user.organisation')),
            ],
        ),
        migrations.AddField(
            model_name='organisation',
            name='wallet',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organisation', to='user.wallet'),
        ),
        migrations.CreateModel(
            name='EmployeeOrganisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_by', models.CharField(blank=True, max_length=150, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_organisation', to='user.employee')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_org', to='user.organisation')),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_wallet', to='user.wallet')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_by', models.CharField(blank=True, max_length=150, null=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('activity_type', models.CharField(choices=[('changed_pin', 'Changed PIN'), ('add_employee', 'Added Employee'), ('add_admin', 'Added Admin'), ('remove_employee', 'Removed Employee'), ('remove_admin', 'Removed Admin'), ('re_activated_employee', 'ReActivated Employee'), ('set_pin', 'Set Pin')], max_length=55)),
                ('is_organisation', models.BooleanField(default=True)),
                ('user_affected', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_log', to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_log_wallet', to='user.wallet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='organisationadmin',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('admin', 'organisation'), name='unique_admin_organisation'),
        ),
        migrations.AddConstraint(
            model_name='employeeorganisation',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('employee', 'organisation'), name='unique_employee_organisation'),
        ),
    ]