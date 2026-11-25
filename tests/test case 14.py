
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
    driver.get("https://www.cynbit.in/")
    time.sleep(4)

    print("\n========== BUTTON AND CTA TESTING ==========")

    buttons = driver.find_elements(
        By.XPATH, "//button | //a"
    )

    print("Total buttons and links:", len(buttons))

    visible_count = 0
    enabled_count = 0

    for index, element in enumerate(buttons, start=1):

        if element.is_displayed():

            visible_count += 1

            text = element.text.strip()
            tag = element.tag_name
            url = element.get_attribute("href")

            enabled = element.is_enabled()

            if enabled:
                enabled_count += 1

            print("\nElement:", index)
            print("Tag:", tag)
            print("Text:", text)
            print("URL:", url)
            print("Visible:", element.is_displayed())
            print("Enabled:", enabled)

    print("\n========== TEST SUMMARY ==========")
    print("Total elements:", len(buttons))
    print("Visible elements:", visible_count)
    print("Enabled visible elements:", enabled_count)

    print("\nButton and CTA inspection completed.")

finally:
    driver.quit()
