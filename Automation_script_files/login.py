from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# Navigate to the login page
driver.get("https://my.replika.ai/login")

# Find the email and password input fields
email_field = driver.find_element_by_name("email")
password_field = driver.find_element_by_name("password")

# Enter your email and password
email_field.send_keys("farazuddin.m1999@gmail.com")
password_field.send_keys("hussnafarha1")

# Press the Enter key to submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(5)

# Close the browser
driver.quit()
