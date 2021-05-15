from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get('http://localhost:5000/')

driver.implicitly_wait(10)

# Find submit button using css seelector and click it
time.sleep(5)
submit_btn = driver.find_element_by_css_selector(".submit-button").click()
print("submit is clicked")

font_element_text = driver.find_element_by_css_selector("#showText").find_element_by_css_selector("font").text

if font_element_text == "Thanks for logging in! Enjoy":
    print("Submit button is clicked correctly!")


while True:
    time.sleep(1)

driver.quit()