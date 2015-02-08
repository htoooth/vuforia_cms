from django.test import LiveServerTestCase
from selenium import webdriver
import unittest

class NewVistorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_to_login(self):
        # Edith has heard about a cool CMS.
        # She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention login page.
        self.assertIn('Login', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Vuforia CMS', header_text)

        # Check URL & current_url & assertRegex()
        this_url = self.browser.current_url
        self.assertRegex(this_url, '/$')

        # Django test client
        # Check if the template is used.
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'login.html')

        # She types "1" into "ユーザーID" box.

        # She types "a" into "パスワード" box.

        # She clicks "Connection" button.

        # She notices the page title and header mention account list page.

        # Satisfied, she goes back to sleep.

        self.fail('Finish the test')

