
import time
import requests

from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://www.cynbit.in/"
DOMAIN = "www.cynbit.in"

results = []


def record(test_name, status, details):
    results.append({
        "test": test_name,
        "status": status,
        "details": details
    })
    print(f"{status}: {test_name} - {details}")


# Start Chrome
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()
wait = WebDriverWait(driver, 10)


try:

    # TC01: Homepage loading

    driver.get(BASE_URL)
    wait.until(
        lambda d: d.find_element(By.TAG_NAME, "body")
    )

    if driver.current_url.startswith(BASE_URL):
        record("TC01 Homepage Loading", "PASS", driver.current_url)
    else:
        record("TC01 Homepage Loading", "FAIL", driver.current_url)

    time.sleep(2)

    # TC02: Page title

    if driver.title.strip():
        record("TC02 Page Title", "PASS", driver.title)
    else:
        record("TC02 Page Title", "FAIL", "Page title is empty")

    # TC03: Cynbit logo


    logos = driver.find_elements(
        By.XPATH, "//img[@alt='Cynbit Logo']"
    )

    if logos and logos[0].is_displayed():
        record("TC03 Logo Visibility", "PASS", "Logo is visible")
    else:
        record("TC03 Logo Visibility", "FAIL", "Logo not visible")

    # TC04: Discover internal website links

    all_links = driver.find_elements(By.TAG_NAME, "a")

    internal_urls = set()

    for link in all_links:
        href = link.get_attribute("href")

        if href:
            parsed = urlparse(href)

            if parsed.netloc in [DOMAIN, "cynbit.in"]:
                clean_url = parsed._replace(
                    fragment=""
                ).geturl()

                internal_urls.add(clean_url)

    print("\nInternal links discovered:", len(internal_urls))

    record(
        "TC04 Internal Link Discovery",
        "INFO",
        f"{len(internal_urls)} internal links found"
    )


    # TC05: Check internal links


    for url in sorted(internal_urls):

        try:
            response = requests.get(
                url,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            if response.status_code < 400:
                record(
                    "TC05 Link Status",
                    "PASS",
                    f"{response.status_code} - {url}"
                )
            else:
                record(
                    "TC05 Link Status",
                    "FAIL",
                    f"{response.status_code} - {url}"
                )

        except requests.RequestException as error:
            record(
                "TC05 Link Status",
                "ERROR",
                f"{url} - {error}"
            )


    # TC06: Open discovered internal pages

    for url in sorted(internal_urls):

        try:
            driver.get(url)

            wait.until(
                lambda d: d.find_element(By.TAG_NAME, "body")
            )

            if driver.find_element(By.TAG_NAME, "body").is_displayed():
                record(
                    "TC06 Page Navigation",
                    "PASS",
                    driver.current_url
                )
            else:
                record(
                    "TC06 Page Navigation",
                    "FAIL",
                    url
                )

        except Exception as error:
            record(
                "TC06 Page Navigation",
                "ERROR",
                f"{url} - {error}"
            )

    # TC07: Check homepage images

    driver.get(BASE_URL)
    time.sleep(3)

    images = driver.find_elements(By.TAG_NAME, "img")

    for index, image in enumerate(images, start=1):

        image_status = driver.execute_script(
            "return arguments[0].complete && "
            "arguments[0].naturalWidth > 0;",
            image
        )

        if image_status:
            record(
                "TC07 Image Loading",
                "PASS",
                f"Image {index} loaded"
            )
        else:
            record(
                "TC07 Image Loading",
                "FAIL",
                f"Image {index} may be broken"
            )


    # TC08: Check buttons and CTAs

    buttons = driver.find_elements(
        By.XPATH, "//button | //a"
    )

    visible_buttons = 0

    for button in buttons:
        if button.is_displayed():
            visible_buttons += 1

    record(
        "TC08 Visible Buttons and Links",
        "INFO",
        f"{visible_buttons} visible elements found"
    )


    # TC09: Check forms and input fields

    forms = driver.find_elements(By.TAG_NAME, "form")
    inputs = driver.find_elements(
        By.XPATH,
        "//input | //textarea | //select"
    )

    record(
        "TC09 Forms and Inputs",
        "INFO",
        f"Forms: {len(forms)}, Input fields: {len(inputs)}"
    )

    # We do not submit forms automatically.
    # Submitting could send real messages or requests.

    # TC10: Responsive layout checks

    screen_sizes = [
        ("Desktop", 1366, 768),
        ("Tablet", 768, 1024),
        ("Mobile", 390, 844)
    ]

    for device, width, height in screen_sizes:

        driver.set_window_size(width, height)
        driver.get(BASE_URL)
        time.sleep(2)

        layout_width = driver.execute_script(
            "return document.documentElement.scrollWidth;"
        )

        viewport_width = driver.execute_script(
            "return window.innerWidth;"
        )

        if layout_width <= viewport_width:
            record(
                f"TC10 Responsive - {device}",
                "PASS",
                f"Viewport: {viewport_width}, Page: {layout_width}"
            )
        else:
            record(
                f"TC10 Responsive - {device}",
                "FAIL",
                f"Horizontal overflow: Page {layout_width}, "
                f"Viewport {viewport_width}"
            )


    # TC11: Restore browser size


    driver.maximize_window()

finally:

    # Save audit report

    with open(
            "../reports/cynbit_audit_results.txt",
        "w",
        encoding="utf-8"
    ) as report:

        for result in results:
            report.write(
                f"{result['status']} | "
                f"{result['test']} | "
                f"{result['details']}\n"
            )

    passed = sum(
        1 for result in results
        if result["status"] == "PASS"
    )

    failed = sum(
        1 for result in results
        if result["status"] == "FAIL"
    )

    print("\n========== AUDIT SUMMARY ==========")
    print("Total checks:", len(results))
    print("Passed:", passed)
    print("Failed:", failed)
    print("===================================")

    print("Report saved as cynbit_audit_results.txt")

    driver.quit()
