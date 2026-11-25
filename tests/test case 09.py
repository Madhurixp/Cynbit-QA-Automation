

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

    print("\n========== REQUIRED FIELD TESTING ==========")

    form = driver.find_element(By.TAG_NAME, "form")

    fields = driver.find_elements(
        By.XPATH, "//form//input | //form//textarea"
    )

    for index, field in enumerate(fields, start=1):

        field.clear()

        is_required = field.get_attribute("required") is not None

        is_valid = driver.execute_script(
            "return arguments[0].checkValidity();", field
        )

        print("\nField:", index)
        print("Placeholder:", field.get_attribute("placeholder"))
        print("Required:", is_required)
        print("Valid when empty:", is_valid)

        if is_required and not is_valid:
            print("PASS: Required field rejects empty value")

        elif not is_required:
            print("INFO: Field is optional")

        else:
            print("FAIL: Required field accepts empty value")

    driver.save_screenshot("required_field_test.png")

finally:
    driver.quit()
