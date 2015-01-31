from selenium import webdriver
import unittest

class NewVistorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_to_login(self):
        # Edith has heard about a cool CMS.
        # She goes to check out its homepage.
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention login page.
        self.assertIn('Login', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Vuforia CMS', header_text)

        # She types "1" into "ユーザーID" box.

        # She types "a" into "パスワード" box.

        # She clicks "Connection" button.

        # She notices the page title and header mention account list page.

        # Satisfied, she goes back to sleep.

        self.fail('Finish the test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
