from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import EmployeeOrganisation, Employee


class EmployeeTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_employee_get_dashboard(self):
        organisation1_sign_up_data = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        organisation1_login_data = {
            "email": "company1@user.com",
            "password": "testpassword",
        }

        admin1_login_data = {
            "email": "admin1@user.com",
            "password": "testpassword",
        }

        organisation1_admin_data = {
            "full_name": "Admin One",
            "email": "admin1@user.com"
        }

        good_data = {
            "full_name": "Employee Five",
            "email": "employee5@user.com"
        }

        # organisation signs up
        self.client.post(reverse('rest_register'), data=organisation1_sign_up_data, format='json')

        # organisation1 login to get access token
        login_org1 = self.client.post(reverse('rest_login'), data=organisation1_login_data, format='json')
        organisation1_access_token = login_org1.data.get('access_token')

        # organisation 1 adds admin 1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        self.client.post(reverse('organisation-add-admin'), data=organisation1_admin_data,
                         format='json')
        self.client.credentials()

        # admin1 login to get access token
        login_admin1 = self.client.post(reverse('rest_login'), data=admin1_login_data, format='json')
        admin1_access_token = login_admin1.data.get('access_token')

        # organisation admin add employee with good data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin1_access_token))
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee added successfully with default password: testpassword')

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        # added employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # organisation admin tries to get employee dashboard
        response = self.client.get(reverse('individual-dashboard'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

        # organisation super admin tires to get employee dashboard
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.get(reverse('individual-dashboard'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

        # employee tries to get dashboard
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.get(reverse('individual-dashboard'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('number_of_organisation'), 1)
        self.assertEqual(response.data.get('number_of_active_organisation'), 1)
        self.assertEqual(response.data.get('number_of_inactive_organisation'), 0)
        # check wallet is created for employee
        self.assertIsNotNone(EmployeeOrganisation.objects.get(organisation__name="Company group",
                                                              employee__user__email="employee5@user.com").wallet)
        # Check wallet balance is 0
        self.assertEqual(response.data.get('active_organisations')[0].get('wallet_balance'), 0)
        self.client.credentials()

    def test_employee_update_profile(self):
        organisation1_sign_up_data = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        organisation1_login_data = {
            "email": "company1@user.com",
            "password": "testpassword",
        }

        admin1_login_data = {
            "email": "admin1@user.com",
            "password": "testpassword",
        }

        organisation1_admin_data = {
            "full_name": "Admin One",
            "email": "admin1@user.com"
        }

        good_data = {
            "full_name": "Employee Five",
            "email": "employee5@user.com"
        }

        good_data2 = {
            "full_name": "Employee Six",
            "email": "employee6@user.com"
        }

        good_update_data = {
            "full_name": "Employee Five Updated",
            "date_of_birth": "2000-12-31",
            "image": "qwerty.s3bucket.amazonaws.com.jpg"
        }

        bad_update_data = {
            "full_name": "Employee",
            "date_of_birth": "2000-12-31",
            "image": "qwerty.s3bucket.amazonaws.com.jpg"
        }

        # organisation signs up
        self.client.post(reverse('rest_register'), data=organisation1_sign_up_data, format='json')

        # organisation1 login to get access token
        login_org1 = self.client.post(reverse('rest_login'), data=organisation1_login_data, format='json')
        organisation1_access_token = login_org1.data.get('access_token')

        # organisation 1 adds admin 1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        self.client.post(reverse('organisation-add-admin'), data=organisation1_admin_data,
                         format='json')
        self.client.credentials()

        # admin1 login to get access token
        login_admin1 = self.client.post(reverse('rest_login'), data=admin1_login_data, format='json')
        admin1_access_token = login_admin1.data.get('access_token')

        # organisation admin add employee with good data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin1_access_token))
        self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')

        # add employee 2
        self.client.post(reverse('organisation-add-employee'), data=good_data2,
                         format='json')

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        employee2_login_data = {
            "email": "employee6@user.com",
            "password": "testpassword",
        }

        # added employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # employee 2 logins
        login_employee2 = self.client.post(reverse('rest_login2'), data=employee2_login_data, format='json')
        employee2_access_token = login_employee2.data.get('access_token')

        # organisation admin tries to update employee profile
        employee = Employee.objects.get(user__email='employee5@user.com')
        response = self.client.patch(reverse('individual-profile', kwargs={'pk': employee.id}), data=good_update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

        # organisation super admin tires to update profile
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.patch(reverse('individual-profile', kwargs={'pk': employee.id}), data=good_update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

        # employee tries to update profile with bad data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.patch(reverse('individual-profile', kwargs={'pk': employee.id}), data=bad_update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Provide employee full name')

        # employee tries updating profile with non existent employee
        response = self.client.patch(reverse('individual-profile', kwargs={'pk': 10000}), data=good_update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Employee does not exist')

        # Employee updates profile with good data
        response = self.client.patch(reverse('individual-profile', kwargs={'pk': employee.id}), data=good_update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('full_name'), 'Employee Five Updated')
        self.client.credentials()

        # employee 2 tires updating data for employee 1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee2_access_token))
        response = self.client.patch(reverse('individual-profile', kwargs={'pk': employee.id}), data=good_update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), "You can't make update for this employee")
        self.client.credentials()
