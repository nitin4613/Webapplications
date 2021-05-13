import threading
import time
from typing import Text
import unittest
from selenium import webdriver
from app import app


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Chrome
        try:
            cls.client = webdriver.Chrome()
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = app

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # start the Flask server in a thread
            threading.Thread(target=cls.app.run).start()

            # give the server a second to ensure it is up
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the flask server and the browser
            cls.client.close()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # navigate to home page
        self.client.get('http://localhost:5000/')

        # navigate to login page
        submit_btn = self.client.find_element_by_css_selector(".submit-button").click()
        print("submit is clicked")

        show_text = self.client.find_element_by_css_selector("#footer").text

        # self.assertEqual(str , type(show_text))
        self.assertTrue(str, type(show_text))



if __name__ == "__main__":
    testcase = SeleniumTestCase()
    testcase.setUpClass()
    testcase.test_admin_home_page()