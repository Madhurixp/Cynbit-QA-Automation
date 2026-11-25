
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()

try:
    driver.get("https://www.cynbit.in/")
    time.sleep(5)

    # Find all images on the homepage
    images = driver.find_elements(By.TAG_NAME, "img")

    print("\n========== IMAGE INVESTIGATION ==========")

    for index, image in enumerate(images, start=1):

        print("\nImage Number:", index)
        print("Image URL:", image.get_attribute("src"))
        print("Alt Text:", image.get_attribute("alt"))

        print(
            "Natural Width:",
            image.get_attribute("naturalWidth")
        )

        print(
            "Natural Height:",
            image.get_attribute("naturalHeight")
        )

finally:
    driver.quit()
