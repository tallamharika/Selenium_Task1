from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import os
from datetime import datetime

# ================== CONFIG ================== #
URL = "https://the-internet.herokuapp.com/login"
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"
WAIT_TIME = 10
LOG_FILE = "execution.log"
SCREENSHOT_FOLDER = "screenshots"

# ================= LOGGING ================== #
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ================ UTILITIES ================= #
def initialize_browser():
    logging.info("Launching Firefox browser")
    driver = webdriver.Firefox()
    driver.maximize_window()
    return driver

def capture_screenshot(driver, reason):
    if not os.path.exists(SCREENSHOT_FOLDER):
        os.mkdir(SCREENSHOT_FOLDER)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{SCREENSHOT_FOLDER}/{reason}_{timestamp}.png"
    driver.save_screenshot(file_name)
    logging.info(f"Screenshot captured: {file_name}")

# ================== TESTS =================== #
def login_test(driver):
    logging.info("Starting Login Test")
    driver.get(URL)
    wait = WebDriverWait(driver, WAIT_TIME)

    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    message = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
    assert "secure area" in message.lower()
    print("✅ Login test passed")

def logout_test(driver):
    logging.info("Starting Logout Test")
    wait = WebDriverWait(driver, WAIT_TIME)

    driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius").click()
    message = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
    assert "logged out" in message.lower()
    print("✅ Logout test passed")

# ================== MAIN ==================== #
def main():
    driver = initialize_browser()
    try:
        login_test(driver)
        logout_test(driver)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY")
        logging.info("All tests passed successfully")
    except (TimeoutException, AssertionError) as error:
        logging.error(f"Test failed: {error}")
        capture_screenshot(driver, "test_failure")
        print("❌ Test failed — screenshot captured")
    finally:
        driver.quit()
        logging.info("Browser closed")

if __name__ == "__main__":
    main()
