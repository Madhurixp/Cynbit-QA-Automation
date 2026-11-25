
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

    time.sleep(4)

    print("\n========== CONTACT FORM INVESTIGATION ==========")

    fields = driver.find_elements(
        By.XPATH,
        "//input | //textarea | //select"
    )

    for index, field in enumerate(fields, start=1):

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            field
        )

        time.sleep(1)

        print("\nField:", index)
        print("Placeholder:", field.get_attribute("placeholder"))
        print("Visible:", field.is_displayed())
        print("Enabled:", field.is_enabled())

        print(
            "CSS Display:",
            field.value_of_css_property("display")
        )

        print(
            "CSS Visibility:",
            field.value_of_css_property("visibility")
        )

        print(
            "CSS Opacity:",
            field.value_of_css_property("opacity")
        )

    driver.save_screenshot("contact_form_investigation.png")

finally:
    driver.quit()
