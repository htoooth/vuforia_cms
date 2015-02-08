import logging
from datetime import datetime
from unittest import skip
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.http import HttpRequest
from django.template.loader import render_to_string

from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser
from cms.views.session import login_view

User = get_user_model()
IDENTIFIER_1 = 'ad-00000001'
IDENTIFIER_2 = 'ag-00000001'
IDENTIFIER_3 = 'co-00000001'
USER_1_PASS = 'adminpassw'
USER_2_PASS = 'agencypass'
USER_3_PASS = 'companypas'

class LoginViewTest(TestCase):

    def setUp(self):
        self.userprofile1 = User.objects.create_user(
            acc_type_id=1, parent_admin_id=1, parent_agency_id=None,
            enterprise="test_enterprise", person="test_person",
            address="test_address", email="test@com",
            phone_number="080-1111-2222", password=USER_1_PASS
        )

    #def tearDown(self):

    def test_django_test(self):
        request = HttpRequest()
        response = login_view(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Login</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))

    # TODO
    @skip
    def test_login_page_returns_correct_html(self):
        request = HttpRequest()
        response = login_view(request)
        expected_html = render_to_string('login.html')
        # expected_htmlは、フォームオブジェクトの所が表示されない。
        # render_to_string()でテンプレートタグの部分をどう扱うのか。
        # cf. 「TDD with Python」p.43
        self.assertEqual(response.content.decode(), expected_html)

    # TODO
    # AttributeError: 'HttpRequest' object has no attribute 'session
    # cf. 「TDD with Python」p.54
    @skip
    def test_login_page_can_post_a_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['user_id'] = '1'
        request.POST['acc_type_id'] = '1'
        request.POST['password'] = USER_1_PASS
        response = login_view(request)
        self.assertIn('ログイン中です', response.content.decode())

