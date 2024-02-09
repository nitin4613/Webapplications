import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app



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
            cls.app = create_app()
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

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
            cls.client.get('http://localhost:5000/shutdown')
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
        submit_btn = self.client.find_element(".submit-button").click()
        font_element_text = self.client.find_element_by_css_selector("#showText").find_element_by_css_selector("font").text
        self.assertTrue(re.search('Thanks for logging in! Enjoy', font_element_text))

    def test_FirstName(self):
        # navigate to home page and verify string tag firstname
        self.client.get('http://localhost:5000/')
        font_element_fname = self.client.find_element("fname")
        self.assertTrue(font_element_fname)
    
    def test_MiddleName(self):
        # navigate to home page and verify string tag firstname
        self.client.get('http://localhost:5000/')
        font_element_mname = self.client.find_element("mname")
        self.assertTrue(font_element_mname)

    def test_LastName(self):
        # navigate to home page and verify string tag firstname
        self.client.get('http://localhost:5000/')
        font_element_lname = self.client.find_element("lname")
        self.assertTrue(font_element_lname)