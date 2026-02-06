from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Open Firefox browser
driver = webdriver.Firefox()

# Open sample web application
driver.get("https://the-internet.herokuapp.com/login")
driver.maximize_window()
time.sleep(2)

# LOGIN FUNCTIONALITY
driver.find_element(By.ID, "username").send_keys("tomsmith")
driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(3)

# Verify login
print("Login Message:",
      driver.find_element(By.ID, "flash").text)

# NAVIGATION FUNCTIONALITY (Logout)
driver.find_element(By.CSS_SELECTOR,
                    "a.button.secondary.radius").click()
time.sleep(2)
# Verify navigation
print("Logout Message:",
      driver.find_element(By.ID, "flash").text)

# Close browser
driver.quit()
