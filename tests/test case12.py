
import time
import requests
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
    time.sleep(3)

    print("\n========== BROKEN LINKS TESTING ==========")

    links = driver.find_elements(By.XPATH, "//a[@href]")

    checked_urls = set()

    passed = 0
    failed = 0

    for link in links:

        url = link.get_attribute("href")

        if not url:
            continue

        if not url.startswith("https://www.cynbit.in/"):
            continue

        if url in checked_urls:
            continue

        checked_urls.add(url)

        try:
            response = requests.get(url, timeout=15)

            print("\nURL:", url)
            print("HTTP Status:", response.status_code)

            if response.status_code == 200:
                print("PASS: Link is working")
                passed += 1

            else:
                print("FAIL: Link returned an unsuccessful status")
                failed += 1

        except requests.exceptions.RequestException as error:

            print("\nURL:", url)
            print("FAIL: Request error:", error)
            failed += 1

    print("\n========== TEST SUMMARY ==========")
    print("Unique links checked:", len(checked_urls))
    print("Passed:", passed)
    print("Failed:", failed)

finally:
    driver.quit()

