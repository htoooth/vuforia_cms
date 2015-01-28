import logging
from datetime import datetime
from unittest import skip
from unittest.mock import patch
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser

User = get_user_model()
IDENTIFIER_1 = 'ad-00000001'
IDENTIFIER_2 = 'ag-00000001'
IDENTIFIER_3 = 'co-00000001'
USER_1_PASS = 'adminpassw'
USER_2_PASS = 'agencypass'
USER_3_PASS = 'companypas'

class ModelTest(TestCase):

    def setUp(self):
        self.userprofile1 = User.objects.create_user(
            acc_type_id=1, parent_admin_id=1, parent_agency_id=None,
            enterprise="test_enterprise", person="test_person",
            address="test_address", email="test@com",
            phone_number="080-1111-2222", password=USER_1_PASS
        )

    def test_set_userprofile_identifier_for_admin(self):
        self.assertEqual(IDENTIFIER_1, self.userprofile1.identifier)

    def test_set_userprofile_identifier_for_agency(self):
        userprofile2 = User.objects.create_user(
            acc_type_id=2, parent_admin_id=1, parent_agency_id=None,
            enterprise="test_enterprise", person="test_person",
            address="test_address", email="test@com",
            phone_number="080-1111-2222", password=USER_2_PASS
        )
        self.assertEqual(IDENTIFIER_2, userprofile2.identifier)

    def test_set_userprofile_identifier_for_company(self):
        userprofile3 = User.objects.create_user(
            acc_type_id=3, parent_admin_id=1, parent_agency_id=None,
            enterprise="test_enterprise", person="test_person",
            address="test_address", email="test@com",
            phone_number="080-1111-2222", password=USER_3_PASS
        )
        self.assertEqual(IDENTIFIER_3, userprofile3.identifier)

    def test_set_hashed_password(self):
        self.assertEqual(77, len(self.userprofile1.password))

    def test_set_user_relative_to_created_userprofile(self):
        self.assertEqual(1, AdminUser.objects.get(id=1).user_profile_id)

    def test_delete_userprofile(self):
        self.userprofile1.delete()
        self.assertFalse(UserProfile.objects.all())

    def test_delete_user_relative_to_the_userprofile(self):
        self.assertTrue(AdminUser.objects.all())
        self.userprofile1.delete()
        self.assertFalse(AdminUser.objects.all())

    # TODO: delete relation objects
    #       when UserProfile objects in bulk are deleted
    @skip
    def test_delete_all_the_users_when_delete_userprofile_in_bulk(self):
        for i in range(3):
            User.objects.create_user(
                acc_type_id=1, parent_admin_id=1, parent_agency_id=None,
                enterprise="test_enterprise", person="test_person",
                address="test_address", email="test@com",
                phone_number="080-1111-2222", password=USER_1_PASS
            )
        self.assertEqual(4, len(User.objects.all()))
        User.objects.all().delete()
        self.assertFalse(AdminUser.objects.all())

class AuthenticateTest(TestCase):
    def setUp(self):
        self.userprofile1 = User.objects.create_user(
            acc_type_id=1, parent_admin_id=1, parent_agency_id=None,
            enterprise="test_enterprise", person="test_person",
            address="test_address", email="test@com",
            phone_number="080-1111-2222", password=USER_1_PASS
        )

    def test_authenticate_method(self):
        authenticated_userprofile = authenticate(identifier=IDENTIFIER_1,
                                                 password=USER_1_PASS)
        self.assertEqual(self.userprofile1, authenticated_userprofile)

    def test_login_method(self):
        before1 = UserProfile.objects.get(id=1).last_login
        self.client.post('/', {'user_id': 1,
                               'acc_type_id': 1,
                               'password': USER_1_PASS}
        )
        self.assertNotEqual(before1, UserProfile.objects.get(id=1).last_login)

