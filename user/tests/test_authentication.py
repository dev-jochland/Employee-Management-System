from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import user.models as um


class OrganisationSignUpTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_organisation_can_sign_up(self):
        good_data = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        data_without_full_name = {
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        data_with_invalid_full_name = {
            "full_name": "Company",
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        data_without_company_name = {
            "full_name": "Company One",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        data_without_valid_email = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        data_without_email = {
            "full_name": "Company One",
            "company_name": "Company group",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        data_without_role = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1@user.com",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        data_without_password1 = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password2": "testpassword"
        }

        data_without_password2 = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword"
        }

        data_without_matching_password = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword1"
        }

        existing_company_name = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company11@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        existing_email = {
            "full_name": "Company One",
            "company_name": "Company groups",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        # Organisation tried registering without full name
        response = self.client.post(reverse('rest_register'), data=data_without_full_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field full_name is required')

        # Organisation tried registering with invalid full name
        response = self.client.post(reverse('rest_register'), data=data_with_invalid_full_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Please provide your first name and last name')

        # Organisation tried registering without role
        response = self.client.post(reverse('rest_register'), data=data_without_role, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field role is required')

        # Organisation tried registering without company name
        response = self.client.post(reverse('rest_register'), data=data_without_company_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field company_name is required')

        # Organisation tried registering without email
        response = self.client.post(reverse('rest_register'), data=data_without_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field email is required')

        # Organisation tried registering without password1
        response = self.client.post(reverse('rest_register'), data=data_without_password1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field password1 is required')

        # Organisation tried registering without password2
        response = self.client.post(reverse('rest_register'), data=data_without_password2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field password2 is required')

        # Organisation tried registering without valid email
        response = self.client.post(reverse('rest_register'), data=data_without_valid_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Enter a valid email address.')

        # Organisation tried registering without matching passwords
        response = self.client.post(reverse('rest_register'), data=data_without_matching_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'The two password fields didn\'t match.')

        # Organisation tried registering with good data
        response = self.client.post(reverse('rest_register'), data=good_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employer successfully onboarded with initial amount of nine '
                                                      'hundred and ninety nine trillion (999999999999999). '
                                                      'Please login to continue')

        # check wallet was created for organisation
        self.assertIsNotNone(um.Organisation.objects.get(name="Company group").wallet)

        # check admin object is created for email just onboarded
        self.assertIsNotNone(um.Admin.objects.get(user__email='company1@user.com'))

        # check super admin object is created for this email
        self.assertIsNotNone(um.OrganisationAdmin.objects.get(organisation__name="Company group",
                                                              admin__user__email='company1@user.com',
                                                              admin_type='super_admin'))

        # Another Organisation tried registering with existing company name
        response = self.client.post(reverse('rest_register'), data=existing_company_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Company name already exists')

        # Another Organisation tried registering with existing email
        response = self.client.post(reverse('rest_register'), data=existing_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'A user is already registered with this e-mail address.')


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_organisation_can_log_in(self):
        good_data = {
            "email": "company1@user.com",
            "password": "testpassword",
        }

        data_without_email = {
            "password": "testpassword",
        }

        data_without_password = {
            "email": "company1@user.com",
        }

        non_admin_email = {
            "email": "user1@user.com",
            "password": "testpassword",
        }

        data_with_wrong_auth_details = {
            "email": "company1@user.com",
            "password": "testpassword234",
        }

        sign_up_data = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        # Organisation onboards
        response = self.client.post(reverse('rest_register'), data=sign_up_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'Employer successfully onboarded with initial amount of nine '
                                                      'hundred and ninety nine trillion (999999999999999). '
                                                      'Please login to continue')

        # Organisation tried authenticating without email
        response = self.client.post(reverse('rest_login'), data=data_without_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field email is required')

        # Organisation tried authenticating without password
        response = self.client.post(reverse('rest_login'), data=data_without_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field password is required')

        # Non admin email tries signing up
        response = self.client.post(reverse('rest_login'), data=non_admin_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'You are not an admin')

        # Organisation tried authenticating with wrong auth details
        response = self.client.post(reverse('rest_login'), data=data_with_wrong_auth_details, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Unable to log in with provided credentials.')

        # Organisation tried authenticating with good data
        login_response = self.client.post(reverse('rest_login'), data=good_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Check access token is returned
        self.assertIsNotNone(login_response.data.get('access_token'))

        # Check refresh token is returned
        self.assertIsNotNone(login_response.data.get('refresh_token'))

        employee_data = {
            "full_name": "Employee Five",
            "email": "employee5@user.com"
        }

        admin_data = {
            "full_name": "Admin One",
            "email": "admin1@user.com"
        }

        login_admin_data = {
            "email": "admin1@user.com",
            "password": "testpassword"
        }

        login_employee_data = {
            "email": "employee5@user.com",
            "password": "testpassword"
        }

        # organisation add employee
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(login_response.data.get('access_token')))
        response = self.client.post(reverse('organisation-add-employee'), data=employee_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # organisation add admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(login_response.data.get('access_token')))
        response = self.client.post(reverse('organisation-add-admin'), data=admin_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

        # Admin logs in
        admin_login_response = self.client.post(reverse('rest_login'), data=login_admin_data, format='json')
        self.assertEqual(admin_login_response.status_code, status.HTTP_200_OK)

        # Check access token is returned
        self.assertIsNotNone(admin_login_response.data.get('access_token'))

        # Check refresh token is returned
        self.assertIsNotNone(admin_login_response.data.get('refresh_token'))

        # employee logs in
        employee_login_response = self.client.post(reverse('rest_login2'), data=login_employee_data, format='json')
        self.assertEqual(employee_login_response.status_code, status.HTTP_200_OK)

        # Check access token is returned
        self.assertIsNotNone(employee_login_response.data.get('access_token'))

        # Check refresh token is returned
        self.assertIsNotNone(employee_login_response.data.get('refresh_token'))


class ChangePasswordTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_change_password(self):
        sign_up_data = {
            "full_name": "Company One",
            "company_name": "Company group",
            "email": "company1@user.com",
            "role": "CEO",
            "password1": "testpassword",
            "password2": "testpassword"
        }

        good_data = {
            "email": "company1@user.com",
            "password": "testpassword",
        }

        good_password_data = {
            "old_password": "testpassword",
            "new_password1": "testpassword1",
            "new_password2": "testpassword1"
        }

        password_data_without_old_password = {
            "new_password1": "testpassword",
            "new_password2": "testpassword"
        }

        password_data_with_incorrect_old_password = {
            "old_password": "testpassword1",
            "new_password1": "testpassword",
            "new_password2": "testpassword"
        }

        password_data_without_new_password1 = {
            "old_password": "testpassword",
            "new_password2": "testpassword"
        }

        password_data_without_new_password2 = {
            "old_password": "testpassword",
            "new_password1": "testpassword",
        }

        password_data_not_match = {
            "old_password": "testpassword",
            "new_password1": "testpassword1",
            "new_password2": "testpassword2"
        }

        # Organisation onboards
        response = self.client.post(reverse('rest_register'), data=sign_up_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Organisation tries changing password without authenticating
        response = self.client.post(reverse('rest_password_change'), data=good_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

        # Organisation logs in
        login_response = self.client.post(reverse('rest_login'), data=good_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # organisation tries changing password without old password
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(login_response.data.get('access_token')))
        response = self.client.post(reverse('rest_password_change'), data=password_data_without_old_password,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field old_password is required')

        # organisation tries changing password without new password1
        response = self.client.post(reverse('rest_password_change'), data=password_data_without_new_password1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field new_password1 is required')

        # organisation tries changing password with incorrect old password
        response = self.client.post(reverse('rest_password_change'), data=password_data_with_incorrect_old_password,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Your old password was entered incorrectly. Please enter it '
                                                      'again.')

        # organisation tries changing password without new password2
        response = self.client.post(reverse('rest_password_change'), data=password_data_without_new_password2,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'Field new_password2 is required')

        # organisation tries changing password without password that don't match
        response = self.client.post(reverse('rest_password_change'), data=password_data_not_match,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'The two password fields didn’t match.')

        # organisation tries changing password with good password data
        response = self.client.post(reverse('rest_password_change'), data=good_password_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'New password has been saved.')

        employee_data = {
            "full_name": "Employee Five",
            "email": "employee5@user.com"
        }

        admin_data = {
            "full_name": "Admin One",
            "email": "admin1@user.com"
        }

        login_admin_data = {
            "email": "admin1@user.com",
            "password": "testpassword"
        }

        login_employee_data = {
            "email": "employee5@user.com",
            "password": "testpassword"
        }

        # organisation add employee
        response = self.client.post(reverse('organisation-add-employee'), data=employee_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # organisation add admin
        response = self.client.post(reverse('organisation-add-admin'), data=admin_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

        # Admin logs in
        admin_login_response = self.client.post(reverse('rest_login'), data=login_admin_data, format='json')
        self.assertEqual(admin_login_response.status_code, status.HTTP_200_OK)

        # admin tries changing password with good password data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(admin_login_response.data.get('access_token')))
        response = self.client.post(reverse('rest_password_change'), data=good_password_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'New password has been saved.')
        self.client.credentials()

        # employee logs in
        employee_login_response = self.client.post(reverse('rest_login2'), data=login_employee_data, format='json')
        self.assertEqual(employee_login_response.status_code, status.HTTP_200_OK)

        # employee tries changing password with good password data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(employee_login_response.data.get('access_token')))
        response = self.client.post(reverse('rest_password_change'), data=good_password_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('detail'), 'New password has been saved.')
        self.client.credentials()


