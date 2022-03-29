from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import EmployeeOrganisation, Organisation


class OrganisationSignUpTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        # organisation1_sign_up_data = {
        #     "full_name": "Company One",
        #     "company_name": "Company group",
        #     "email": "company1@user.com",
        #     "role": "CEO",
        #     "password1": "testpassword",
        #     "password2": "testpassword"
        # }
        #
        # organisation2_sign_up_data = {
        #     "full_name": "Company Two",
        #     "company_name": "Company group2",
        #     "email": "company2@user.com",
        #     "role": "CEO",
        #     "password1": "testpassword",
        #     "password2": "testpassword"
        # }
        #
        # organisation1_admin_data = {
        #     "full_name": "Admin One",
        #     "email": "admin1@user.com"
        # }
        #
        # organisation2_admin_data = {
        #     "full_name": "Admin Two",
        #     "email": "admin2@user.com"
        # }
        #
        # organisation1_login_data = {
        #     "email": "company1@user.com",
        #     "password": "testpassword",
        # }
        #
        # organisation2_login_data = {
        #     "email": "company2@user.com",
        #     "password": "testpassword",
        # }
        #
        # admin1_login_data = {
        #     "email": "admin1@user.com",
        #     "password": "testpassword",
        # }
        #
        # admin2_login_data = {
        #     "email": "admin2@user.com",
        #     "password": "testpassword",
        # }
        #
        # employee_data = {
        #     "full_name": "Employee Nine",
        #     "email": "employee9@user.com"
        # }
        #
        # employee_login_data = {
        #     "email": "employee9@user.com",
        #     "password": "testpassword",
        # }
        #
        # # organisation signs up
        # self.client.post(reverse('rest_register'), data=organisation1_sign_up_data, format='json')
        # self.client.post(reverse('rest_register'), data=organisation2_sign_up_data, format='json')
        #
        # # organisation1 login to get access token
        # login_org1 = self.client.post(reverse('rest_login'), data=organisation1_login_data, format='json')
        # self.organisation1_access_token = login_org1.data.get('access_token')
        #
        # # organisation2 login to get access token
        # login_org2 = self.client.post(reverse('rest_login'), data=organisation2_login_data, format='json')
        # self.organisation2_access_token = login_org2.data.get('access_token')
        #
        # # organisation 1 adds admin 1
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.organisation1_access_token))
        # self.client.post(reverse('organisation-add-admin'), data=organisation1_admin_data,
        #                  format='json')
        #
        # # organisation 2 adds admin 2
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.organisation2_access_token))
        # self.client.post(reverse('organisation-add-admin'), data=organisation2_admin_data,
        #                  format='json')
        #
        # # admin1 login to get access token
        # login_admin1 = self.client.post(reverse('rest_login'), data=admin1_login_data, format='json')
        # self.admin1_access_token = login_admin1.data.get('access_token')
        #
        # # admin2 login to get access token
        # login_admin2 = self.client.post(reverse('rest_login'), data=admin2_login_data, format='json')
        # self.admin2_access_token = login_admin2.data.get('access_token')

        # # organisation add employee
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.organisation1_access_token))
        # self.client.post(reverse('organisation-add-employee'), data=employee_data, format='json')
        #
        # # employee login to get access token
        # login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        # self.employee_access_token = login_employee.data.get('access_token')

    def test_add_employee(self):
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

        data_without_full_name = {
            "email": "employee5@user.com"
        }

        data_without_email = {
            "full_name": "Employee Five",
        }

        data_with_invalid_email = {
            "full_name": "Employee Five",
            "email": "employeeuser.com"
        }

        data_with_invalid_full_name = {
            "full_name": "Employee ",
            "email": "employee5@user.com"
        }

        # organisation signs up
        self.client.post(reverse('rest_register'), data=organisation1_sign_up_data, format='json')

        # organisation1 login to get access token
        login_org1 = self.client.post(reverse('rest_login'), data=organisation1_login_data, format='json')
        organisation1_access_token = login_org1.data.get('access_token')

        # organisation add employee without authentication
        response = self.client.post(reverse('organisation-add-employee'), data=good_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        # organisation add employee without full_name
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.post(reverse('organisation-add-employee'), data=data_without_full_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field full_name is required')

        # organisation add employee without email
        response = self.client.post(reverse('organisation-add-employee'), data=data_without_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field email is required')

        # organisation add employee with invalid email
        response = self.client.post(reverse('organisation-add-employee'), data=data_with_invalid_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid email format')

        # organisation add employee with invalid full_name
        response = self.client.post(reverse('organisation-add-employee'), data=data_with_invalid_full_name,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Provide employee full name')

        # organisation add employee with good data
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee added successfully with default password: testpassword')

        # organisation 1 adds admin 1
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'User is already an employee in your organisation')

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        # added employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # added employee tries adding another employee
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

    def test_get_organisation_dashboard(self):
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
        self.client.credentials()

        # organisation add employee with good data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
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

        # super admin get organisation dashboard
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.get(reverse('organisation-dashboard'))
        self.assertEqual(len(response.data.get('active_employees')), 1)
        self.assertEqual(len(response.data.get('inactive_employees')), 0)
        self.assertEqual(response.data.get('wallet_balance'), 999999999999999.0000)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

        # admin get organisation dashboard
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin1_access_token))
        response = self.client.get(reverse('organisation-dashboard'))
        self.assertEqual(len(response.data.get('active_employees')), 1)
        self.assertEqual(len(response.data.get('inactive_employees')), 0)
        self.assertEqual(response.data.get('wallet_balance'), 999999999999999.0000)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

        # added employee tries to get company dashboard
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.get(reverse('organisation-dashboard'), data=good_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

    def test_add_admin(self):
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

        good_admin_data = {
            "full_name": "Admin Ten",
            "email": "employee10@user.com"
        }

        good_data = {
            "full_name": "Employee Five",
            "email": "employee5@user.com"
        }

        data_without_full_name = {
            "email": "employee5@user.com"
        }

        data_without_email = {
            "full_name": "Employee Five",
        }

        data_with_invalid_email = {
            "full_name": "Employee Five",
            "email": "employeeuser.com"
        }

        data_with_invalid_full_name = {
            "full_name": "Employee ",
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
        self.client.credentials()

        # organisation add admin without authentication
        response = self.client.post(reverse('organisation-add-admin'), data=good_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        # organisation add admin without full_name
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.post(reverse('organisation-add-admin'), data=data_without_full_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field full_name is required')

        # organisation add admin without email
        response = self.client.post(reverse('organisation-add-admin'), data=data_without_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field email is required')

        # organisation add admin with invalid email
        response = self.client.post(reverse('organisation-add-admin'), data=data_with_invalid_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Invalid email format')

        # organisation add admin with invalid full_name
        response = self.client.post(reverse('organisation-add-admin'), data=data_with_invalid_full_name,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Provide admin full name')

        # organisation add admin with good data
        response = self.client.post(reverse('organisation-add-admin'), data=good_admin_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Admin added successfully with default password: testpassword')
        self.client.credentials()

        # organisation admin add admin with good data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin1_access_token))
        response = self.client.post(reverse('organisation-add-admin'), data=good_admin_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')

        # organisation admin add employee with good data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin1_access_token))
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee added successfully with default password: testpassword')
        self.client.credentials()

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        # added employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # added employee tries adding admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.post(reverse('organisation-add-admin'), data=good_admin_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

        # organisation tries adding already added admin with good data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.post(reverse('organisation-add-admin'), data=good_admin_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'This email is already registered on the platform')
        self.client.credentials()

    def test_remove_employee(self):
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

        data_without_email = {
        }

        data_with_email = {
            "employee_email": "employee5@user.com"
        }

        data_with_non_exist_email = {
            "employee_email": "employee900@user.com"
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

        # organisation add employee with good data
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee added successfully with default password: testpassword')
        self.client.credentials()

        # admin1 login to get access token
        login_admin1 = self.client.post(reverse('rest_login'), data=admin1_login_data, format='json')
        admin1_access_token = login_admin1.data.get('access_token')
        self.client.credentials()

        # organisation remove employee without authentication
        response = self.client.patch(reverse('organisation-remove-employee'), data=data_with_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        # organisation remove employee without email
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.patch(reverse('organisation-remove-employee'), data=data_without_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field employee_email is required')

        # organisation remove employee that does not exist
        response = self.client.patch(reverse('organisation-remove-employee'), data=data_with_non_exist_email,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'This employee is not part of this organisation')

        # organisation remove employee
        response = self.client.patch(reverse('organisation-remove-employee'), data=data_with_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee deactivated from organisation successfully')
        self.client.credentials()

        # organisation try removing already removed employee
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin1_access_token))
        response = self.client.patch(reverse('organisation-remove-employee'), data=data_with_email,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Employee is already deactivated from organisation')

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        # removed employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # removed employee tries to access remove employee endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.post(reverse('organisation-remove-employee'), data=data_with_email,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

    def test_reactivate_employee(self):
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

        data_without_email = {
        }

        data_with_email = {
            "employee_email": "employee5@user.com"
        }

        data_with_non_exist_email = {
            "employee_email": "employee900@user.com"
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

        # organisation add employee with good data
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee added successfully with default password: testpassword')

        # turn employee is_active to False
        self.client.patch(reverse('organisation-remove-employee'), data=data_with_email, format='json')
        self.client.credentials()

        # admin1 login to get access token
        login_admin1 = self.client.post(reverse('rest_login'), data=admin1_login_data, format='json')
        admin1_access_token = login_admin1.data.get('access_token')
        self.client.credentials()

        # organisation reactivate employee without authentication
        response = self.client.patch(reverse('organisation-reactivate-employee'), data=data_with_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        # organisation reactivate employee without email
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.patch(reverse('organisation-remove-employee'), data=data_without_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field employee_email is required')

        # organisation reactivate employee that does not exist
        response = self.client.patch(reverse('organisation-reactivate-employee'), data=data_with_non_exist_email,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'This employee is not part of this organisation')

        # organisation reactivate employee
        response = self.client.patch(reverse('organisation-reactivate-employee'), data=data_with_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee reactivated to organisation successfully')
        self.client.credentials()

        # organisation try reactivating already activated employee
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin1_access_token))
        response = self.client.patch(reverse('organisation-reactivate-employee'), data=data_with_email,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Employee is already active in your organisation')

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        # removed employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # removed employee tries to access reactivate employee endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.post(reverse('organisation-reactivate-employee'), data=data_with_email,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

    def test_remove_admin(self):
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

        organisation1_admin_data = {
            "full_name": "Admin One",
            "email": "admin1@user.com"
        }

        good_data = {
            "full_name": "Employee Five",
            "email": "employee5@user.com"
        }

        data_without_email = {
        }

        data_with_email = {
            "admin_email": "admin1@user.com"
        }

        data_with_non_exist_email = {
            "admin_email": "employee900@user.com"
        }

        super_admin_email = {
            "admin_email": "company1@user.com",
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

        # organisation add employee with good data
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee added successfully with default password: testpassword')
        self.client.credentials()

        # organisation remove admin without authentication
        response = self.client.patch(reverse('organisation-remove-admin'), data=data_with_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        # organisation remove admin without email
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.patch(reverse('organisation-remove-admin'), data=data_without_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field admin_email is required')

        # organisation remove admin that does not exist
        response = self.client.patch(reverse('organisation-remove-admin'), data=data_with_non_exist_email,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'This admin is not part of this organisation')

        # organisation super admin tries removing itself
        response = self.client.patch(reverse('organisation-remove-admin'), data=super_admin_email,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), "Super admin can\'t remove itself, contact product "
                                                      "administrator.")

        # organisation remove admin
        response = self.client.patch(reverse('organisation-remove-admin'), data=data_with_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), "Admin removed from organisation successfully")

        # organisation try removing already removed admin
        response = self.client.patch(reverse('organisation-remove-admin'), data=data_with_email,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Admin already removed from organisation')

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        # removed employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # removed employee tries to access remove employee endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.post(reverse('organisation-remove-admin'), data=data_with_email,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

    def test_get_all_admins(self):
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

        good_admin_data = {
            "full_name": "Admin Ten",
            "email": "employee10@user.com"
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

        # organisation add admin 2 with good data
        self.client.post(reverse('organisation-add-admin'), data=good_admin_data,
                         format='json')

        # super admin get all admins
        response = self.client.get(reverse('organisation-admins'))
        self.assertEqual(len(response.data), 2)
        self.client.credentials()

        # admin1 login to get access token
        login_admin1 = self.client.post(reverse('rest_login'), data=admin1_login_data, format='json')
        admin1_access_token = login_admin1.data.get('access_token')

        # admin tries getting admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin1_access_token))
        response = self.client.get(reverse('organisation-admins'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')

        # organisation admin add employee with good data
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee added successfully with default password: testpassword')
        self.client.credentials()

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        # added employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # added employee tries getting admins
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.get(reverse('organisation-admins'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()

    def test_update_profile(self):
        organisation1_sign_up_data = {
            "full_name": "Company One",
            "company_name": "Company grouper",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        organisation1_login_data = {
            "email": "company1@user.com",
            "password": "testpassword",
        }

        organisation2_sign_up_data = {
            "full_name": "Company Two",
            "company_name": "Company groupers",
            "email": "company2@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        organisation2_login_data = {
            "email": "company2@user.com",
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

        update_data = {
            "profile": "Organisation profile updated with this sentence"
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

        # organisation add employee with good data
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee added successfully with default password: testpassword')
        self.client.credentials()

        # admin1 login to get access token
        login_admin1 = self.client.post(reverse('rest_login'), data=admin1_login_data, format='json')
        admin1_access_token = login_admin1.data.get('access_token')
        self.client.credentials()

        # organisation update profile without authentication
        organisation = Organisation.objects.get(name='Company grouper')
        response = self.client.patch(reverse('organisation-profile', kwargs={'pk': organisation.id}), data=update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        # organisation update profile
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation1_access_token))
        response = self.client.patch(reverse('organisation-profile', kwargs={'pk': organisation.id}), data=update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

        # organisation admin can also update company profile
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin1_access_token))
        response = self.client.patch(reverse('organisation-profile', kwargs={'pk': organisation.id}), data=update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

        # organisation2 signs up
        self.client.post(reverse('rest_register'), data=organisation2_sign_up_data, format='json')

        # organisation2 login to get access token
        login_org2 = self.client.post(reverse('rest_login'), data=organisation2_login_data, format='json')
        organisation2_access_token = login_org2.data.get('access_token')

        # organisation tries to update profile for organisation1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(organisation2_access_token))
        response = self.client.patch(reverse('organisation-profile', kwargs={'pk': organisation.id}), data=update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials()

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        # employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # employee tries to update company profile
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.patch(reverse('organisation-profile', kwargs={'pk': organisation.id}), data=update_data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials()

    def test_admin_pay_single_employee(self):
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

        # admin1 login to get access token
        login_admin1 = self.client.post(reverse('rest_login'), data=admin1_login_data, format='json')
        admin1_access_token = login_admin1.data.get('access_token')

        # organisation admin add employee with good data
        response = self.client.post(reverse('organisation-add-employee'), data=good_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employee added successfully with default password: testpassword')
        self.client.credentials()

        employee_login_data = {
            "email": "employee5@user.com",
            "password": "testpassword",
        }

        # added employee login to get access token
        login_employee = self.client.post(reverse('rest_login2'), data=employee_login_data, format='json')
        employee_access_token = login_employee.data.get('access_token')

        # added employee tries getting admins
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_access_token))
        response = self.client.get(reverse('organisation-admins'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
        self.client.credentials()
