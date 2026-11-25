
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()

try:
    driver.get("https://www.cynbit.in/contact")
    time.sleep(3)

    print("\n========== CONTACT FORM FUNCTIONAL TESTING ==========")

    # Locate contact form
    form = driver.find_element(By.TAG_NAME, "form")

    # Locate all five fields
    name = driver.find_element(
        By.XPATH, "//input[@placeholder='e.g. Alex Rivera']"
    )

    email = driver.find_element(
        By.XPATH, "//input[@placeholder='alex@example.com']"
    )

    organization = driver.find_element(
        By.XPATH, "//input[@placeholder='Your Organization']"
    )

    industry = driver.find_element(
        By.XPATH, "//input[@placeholder='e.g. Fintech, Healthcare']"
    )

    message = driver.find_element(
        By.XPATH,
        "//textarea[@placeholder='How can we help you architect your next chapter?']"
    )

    # Fill form with valid test data
    name.send_keys("Test User")
    email.send_keys("testuser@example.com")
    organization.send_keys("Test Organization")
    industry.send_keys("Information Technology")
    message.send_keys("This is a test message for QA automation.")

    print("\n--- VALID DATA TEST ---")

    print("Name entered:", name.get_attribute("value"))
    print("Email entered:", email.get_attribute("value"))
    print("Organization entered:", organization.get_attribute("value"))
    print("Industry entered:", industry.get_attribute("value"))
    print("Message entered:", message.get_attribute("value"))

    valid_result = driver.execute_script(
        "return arguments[0].checkValidity();", form
    )

    if valid_result:
        print("PASS: Form accepts valid test data")
    else:
        print("FAIL: Form validation rejected valid test data")

    # Test invalid email
    print("\n--- INVALID EMAIL TEST ---")

    email.clear()
    email.send_keys("invalid-email")

    invalid_result = driver.execute_script(
        "return arguments[0].checkValidity();", form
    )

    if not invalid_result:
        print("PASS: Form rejects invalid email")
    else:
        print("FAIL: Form accepts invalid email")

    print("\nEmail field type:", email.get_attribute("type"))
    print("Email field required:", email.get_attribute("required"))

    driver.save_screenshot("contact_form_functional_test.png")

    print("\nScreenshot saved successfully.")

finally:
    driver.quit()
