
import time
import requests

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

    images = driver.find_elements(By.TAG_NAME, "img")

    print("\n========== SVG ICON TEST ==========")

    for index, image in enumerate(images, start=1):

        image_url = image.get_attribute("src")

        if image_url and ".svg" in image_url:

            response = requests.get(image_url, timeout=15)

            print("\nImage:", index)
            print("URL:", image_url)
            print("HTTP Status:", response.status_code)
            print("Visible:", image.is_displayed())
            print("Image Complete:", image.get_attribute("complete"))
            print("Natural Width:", image.get_attribute("naturalWidth"))

finally:
    driver.quit()
