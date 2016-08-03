from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.auth.models import User
from selenium import webdriver
import time


class IndexPageViewTestCase(StaticLiveServerTestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpClass(cls):
        super(IndexPageViewTestCase, cls).setUpClass()
        cls.selenium = webdriver.PhantomJS()
        cls.selenium.set_window_size(1400, 1000)
        cls.selenium.implicitly_wait(30)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(IndexPageViewTestCase, cls).tearDownClass()

    def test_page_load(self):
        self.selenium.get(self.live_server_url)

        # test page load
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Live your dreams', body.text)

    def test_login(self):
        self.selenium.get(self.live_server_url)

        # test invalid login
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('malikwahab')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_name("signin").click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Username of password Incorrect', body.text)

        # test signup
        self.selenium.find_element_by_css_selector("a[href='#signup']").click()

        username_input = (self.selenium
                          .find_element_by_css_selector("#signup input"
                                                        "[name='username']"))
        username_input.send_keys('malikwahab')
        email_input = (self.selenium
                       .find_element_by_css_selector("#signup input"
                                                     "[name='email']"))
        email_input.send_keys('malik@wahab.com')
        password_input = (self.selenium
                          .find_element_by_css_selector("#signup input"
                                                        "[name='password']"))
        password_input.send_keys('password')
        conf_password_input = (self
                               .selenium.find_element_by_css_selector(
                                "#signup input[name='confirm_password']"))
        conf_password_input.send_keys('password')
        self.selenium.find_element_by_name("signup").click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('buppli', body.text)

        # test logout
        self.selenium.find_element_by_link_text('malikwahab').click()
        self.selenium.find_element_by_link_text('Logout').click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Live your dreams', body.text)

        # test login valid
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('malikwahab')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('password')
        self.selenium.find_element_by_name("signin").click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('buppli', body.text)
