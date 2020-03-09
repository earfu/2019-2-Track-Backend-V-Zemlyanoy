from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class SeleniumTestTry(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        assert username_input is not None
        username_input.send_keys('adm')
        password_input = self.selenium.find_element_by_name("password")
        assert password_input is not None
        password_input.send_keys('admpass')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
