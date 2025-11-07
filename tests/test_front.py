import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytest.fixture(scope="class")
def driver_init(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("driver_init")
class TestWebPage:
    # This method is called before each test method in the class
    def setup_method(self, method):
        # Now it's valid to use self, because it's within an instance method
        self.driver.get("http://localhost:5000")  # Navigate to your desired URL
        print("Setup method: Current URL:", self.driver.current_url)
    def test_initial_visibility_of_elements(self):
        form_display = self.driver.find_element(By.ID, "hideme").is_displayed()
        message_display = self.driver.find_element(By.ID, "showText").is_displayed()
        assert form_display
        assert not message_display

    def test_input_field_text_entry(self):
        fname = self.driver.find_element(By.ID, "fname")
        mname = self.driver.find_element(By.ID, "mname")
        lname = self.driver.find_element(By.ID, "lname")

        fname.send_keys("John")
        mname.send_keys("Quincy")
        lname.send_keys("Adams")

        assert fname.get_attribute('value') == "John"
        assert mname.get_attribute('value') == "Quincy"
        assert lname.get_attribute('value') == "Adams"

    def test_page_load(self):
        self.driver.get("http://localhost:5000/")  # Replace with your actual URL
    print("Current URL:", self.driver.current_url)
    assert "localhost:5000" in self.driver.current_url, "The test did not navigate to the expected URL."

    def test_wait_for_redirect_and_check_title(self):
        self.driver.get("http://localhost:5000/")  # Starting URL that redirects
    # Wait for some known element on the target page to become visible
    WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "knownElementAfterRedirect"))
    )
    assert "Welcome folks Please Register" == self.driver.title, "Page title does not match after redirect."

    def test_direct_navigation_to_page(self):
        self.driver.get("http://localhost:5000/finalPage")  # Directly go to the target page
    assert "Welcome folks Please Register" == self.driver.title, "Page title does not match."
    
    def test_debug_redirection(self):
        self.driver.get("http://localhost:5000/")
    print("After initial navigation:", self.driver.current_url, self.driver.title)
    # Wait for a bit to see if a redirect occurs
    WebDriverWait(self.driver, 10).until(lambda d: d.current_url != "http://localhost:5000/")
    print("After waiting for redirect:", self.driver.current_url, self.driver.title)
    assert "Welcome folks Please Register" == self.driver.title, "Page title does not match after potential redirect."

