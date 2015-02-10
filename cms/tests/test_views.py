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
from cms.views.account import edit

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
            address="test_address", email="a@b.com",
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

    def test_edit_function(self):
        """ django.test.TestCaseの clientを使わない場合
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.userprofile1
        request.POST['acc_type_id'] = '1'
        request.POST['enterprise'] = 'edited'
        request.POST['person'] = 'edited'
        request.POST['address'] = 'edited'
        request.POST['email'] = 'a@b.com'
        request.POST['phone_number'] = 'edited'

        response = edit(request,
             self.userprofile1.acc_type_id, self.userprofile1.user_id)
        """

        # @login_requiredとデコレイトされたビューに入る前に。
        self.client.login(identifier=self.userprofile1.identifier,
                          password=USER_1_PASS)
        response = self.client.post(
            '/account/edit/%s/%s' % (self.userprofile1.acc_type_id,
                                   self.userprofile1.user_id,),
            {'acc_type_id': '1', 'enterprise': 'edited',
                  'person': 'edited', 'address': 'edited',
                  'email': 'a@b.com', 'phone_number': 'edited'}
        )

        self.edited_userprofile1 = User.objects.get(
                acc_type_id=self.userprofile1.acc_type_id,
                user_id=self.userprofile1.user_id)

        self.assertRedirects(response, '/account/list')
        self.assertEqual(self.edited_userprofile1.id, self.userprofile1.id)
        self.assertEqual(self.edited_userprofile1.acc_type_id,
                         self.userprofile1.acc_type_id)
        self.assertEqual(self.edited_userprofile1.enterprise, 'edited')
        self.assertEqual(self.edited_userprofile1.person, 'edited')
        self.assertEqual(self.edited_userprofile1.address, 'edited')
        self.assertEqual(self.edited_userprofile1.email, 'a@b.com')
        self.assertEqual(self.edited_userprofile1.phone_number, 'edited')

    def test_edit_pw_function(self):
        # @login_requiredとデコレイトされたビューに入る前に。
        self.client.login(identifier=self.userprofile1.identifier,
                          password=USER_1_PASS)
        response = self.client.post(
            '/account/edit_pw/%s/%s' % (self.userprofile1.acc_type_id,
                                        self.userprofile1.user_id,),
            {'old_password': USER_1_PASS,
             'new_password1': USER_2_PASS,
             'new_password2': USER_2_PASS}
        )

        self.edited_userprofile1 = User.objects.get(
                acc_type_id=self.userprofile1.acc_type_id,
                user_id=self.userprofile1.user_id)

        """Debug
        print(response.status_code)
        print(response['location'])
        """
        self.assertRedirects(response, '/account/list')
        """Django 1.7 で、パスワード変更後、
        update_session_auth_hash()を使わないと、 ログアウトされ、
        assertionを以下のようにしないと、テストが失敗する。
        self.assertRedirects(response, '/account/list',
                             target_status_code=302)
        """
        self.assertEqual(self.edited_userprofile1.id, self.userprofile1.id)
        self.assertNotEqual(self.edited_userprofile1.password,
                            self.userprofile1.password)

