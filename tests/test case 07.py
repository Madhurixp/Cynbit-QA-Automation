
import time
import requests

from urllib.parse import urlparse, urldefrag

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://www.cynbit.in/"

PAGES = [
    "https://www.cynbit.in/",
    "https://www.cynbit.in/services",
    "https://www.cynbit.in/products",
    "https://www.cynbit.in/bitelevate",
    "https://www.cynbit.in/bitelevate/paths",
    "https://www.cynbit.in/contact",
    "https://www.cynbit.in/careers",
    "https://www.cynbit.in/internship",
    "https://www.cynbit.in/blog",
    "https://www.cynbit.in/case-studies",
    "https://www.cynbit.in/story",
    "https://www.cynbit.in/team",
    "https://www.cynbit.in/impact",
    "https://www.cynbit.in/diaries"
]

results = []


def record(test_name, status, details):

    results.append({
        "test": test_name,
        "status": status,
        "details": details
    })

    print(f"{status}: {test_name} - {details}")


def open_page(url):

    driver.get(url)

    wait.until(
        lambda d: d.find_element(By.TAG_NAME, "body")
    )


# START CHROME

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()

wait = WebDriverWait(driver, 15)


try:

    # ==========================================
    # TC01: HOMEPAGE LOADING
    # ==========================================

    print("\n========== HOMEPAGE TESTING ==========")

    open_page(BASE_URL)

    if driver.current_url.startswith(BASE_URL):
        record("TC01 Homepage Loading", "PASS", driver.current_url)
    else:
        record("TC01 Homepage Loading", "FAIL", driver.current_url)


    # ==========================================
    # TC02: PAGE TITLE
    # ==========================================

    if driver.title.strip():

        record("TC02 Page Title", "PASS", driver.title)

    else:

        record("TC02 Page Title", "FAIL", "Title is empty")


    # ==========================================
    # TC03: LOGO VISIBILITY
    # ==========================================

    logos = driver.find_elements(
        By.XPATH,
        "//img[@alt='Cynbit Logo']"
    )

    visible_logos = [
        logo for logo in logos
        if logo.is_displayed()
    ]

    if visible_logos:

        record("TC03 Logo Visibility", "PASS", "Logo visible")

    else:

        record("TC03 Logo Visibility", "FAIL", "Logo not visible")


    # ==========================================
    # TC04: HEADER VISIBILITY
    # ==========================================

    headers = driver.find_elements(By.TAG_NAME, "header")

    if headers and any(h.is_displayed() for h in headers):

        record("TC04 Header Visibility", "PASS", "Header visible")

    else:

        record("TC04 Header Visibility", "FAIL", "Header not found or hidden")


    # ==========================================
    # TC05: NAVIGATION MENU
    # ==========================================

    nav_links = driver.find_elements(
        By.XPATH,
        "//header//a"
    )

    visible_nav_links = [
        link for link in nav_links
        if link.is_displayed()
    ]

    if visible_nav_links:

        record(
            "TC05 Navigation Menu",
            "PASS",
            f"{len(visible_nav_links)} visible navigation links"
        )

    else:

        record(
            "TC05 Navigation Menu",
            "FAIL",
            "No visible navigation links"
        )


    # ==========================================
    # TC06: INTERNAL LINK DISCOVERY
    # ==========================================

    all_links = driver.find_elements(By.TAG_NAME, "a")

    internal_urls = set()

    for link in all_links:

        href = link.get_attribute("href")

        if href:

            parsed = urlparse(href)

            if parsed.netloc in ["www.cynbit.in", "cynbit.in"]:

                clean_url = urldefrag(href)[0]

                internal_urls.add(clean_url)

    record(
        "TC06 Internal Link Discovery",
        "INFO",
        f"{len(internal_urls)} internal links discovered"
    )


    # ==========================================
    # TC07: INTERNAL LINK STATUS
    # ==========================================

    print("\n========== LINK STATUS TESTING ==========")

    for url in sorted(internal_urls):

        try:

            response = requests.get(
                url,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            if response.status_code < 400:

                record(
                    "TC07 Link Status",
                    "PASS",
                    f"{response.status_code} - {url}"
                )

            else:

                record(
                    "TC07 Link Status",
                    "FAIL",
                    f"{response.status_code} - {url}"
                )

        except requests.RequestException as error:

            record(
                "TC07 Link Status",
                "ERROR",
                f"{url} - {error}"
            )


    # ==========================================
    # TC08: PAGE NAVIGATION
    # ==========================================

    print("\n========== PAGE NAVIGATION TESTING ==========")

    for url in sorted(internal_urls):

        try:

            open_page(url)

            if driver.find_element(By.TAG_NAME, "body").is_displayed():

                record(
                    "TC08 Page Navigation",
                    "PASS",
                    driver.current_url
                )

            else:

                record(
                    "TC08 Page Navigation",
                    "FAIL",
                    url
                )

        except Exception as error:

            record(
                "TC08 Page Navigation",
                "ERROR",
                f"{url} - {error}"
            )


    # ==========================================
    # TC09: IMAGE TESTING
    # ==========================================

    print("\n========== IMAGE TESTING ==========")

    open_page(BASE_URL)

    time.sleep(3)

    images = driver.find_elements(By.TAG_NAME, "img")

    for index, image in enumerate(images, start=1):

        image_url = image.get_attribute("src")

        if not image_url:
            continue

        try:

            response = requests.get(
                image_url,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            if response.status_code == 200:

                record(
                    "TC09 Image URL",
                    "PASS",
                    f"Image {index}: HTTP 200 - {image_url}"
                )

            else:

                record(
                    "TC09 Image URL",
                    "FAIL",
                    f"Image {index}: HTTP {response.status_code}"
                )

        except requests.RequestException as error:

            record(
                "TC09 Image URL",
                "ERROR",
                f"Image {index}: {error}"
            )


    # ==========================================
    # TC10: CONTACT PAGE
    # ==========================================

    print("\n========== CONTACT PAGE TESTING ==========")

    open_page("https://www.cynbit.in/contact")

    record(
        "TC10 Contact Page",
        "PASS",
        driver.current_url
    )


    # ==========================================
    # TC11: CONTACT FORM DISCOVERY
    # ==========================================

    contact_forms = driver.find_elements(By.TAG_NAME, "form")

    record(
        "TC11 Contact Forms",
        "INFO",
        f"Forms found: {len(contact_forms)}"
    )


    # ==========================================
    # TC12: CONTACT INPUT FIELDS
    # ==========================================

    contact_fields = driver.find_elements(
        By.XPATH,
        "//input | //textarea | //select"
    )

    record(
        "TC12 Contact Input Fields",
        "INFO",
        f"Fields found: {len(contact_fields)}"
    )

    for field in contact_fields:

        print(
            "Field:",
            field.tag_name,
            "| Type:",
            field.get_attribute("type"),
            "| Placeholder:",
            field.get_attribute("placeholder"),
            "| Visible:",
            field.is_displayed()
        )


    # ==========================================
    # TC13: CONTACT EMAIL AND PHONE LINKS
    # ==========================================

    contact_links = driver.find_elements(By.TAG_NAME, "a")

    for link in contact_links:

        href = link.get_attribute("href")

        if href and (
            href.startswith("mailto:")
            or href.startswith("tel:")
        ):

            record(
                "TC13 Contact Link",
                "INFO",
                href
            )


    # ==========================================
    # TC14: PRODUCTS PAGE
    # ==========================================

    print("\n========== PRODUCTS TESTING ==========")

    open_page("https://www.cynbit.in/products")

    record(
        "TC14 Products Page",
        "PASS",
        driver.current_url
    )


    # ==========================================
    # TC15: PRODUCTS INPUT FIELDS
    # ==========================================

    product_fields = driver.find_elements(
        By.XPATH,
        "//input | //textarea | //select"
    )

    record(
        "TC15 Products Fields",
        "INFO",
        f"Fields found: {len(product_fields)}"
    )


    # ==========================================
    # TC16: BITELEVATE PAGE
    # ==========================================

    print("\n========== BITELEVATE TESTING ==========")

    open_page("https://www.cynbit.in/bitelevate")

    record(
        "TC16 BitElevate Page",
        "PASS",
        driver.current_url
    )


    # ==========================================
    # TC17: BITELEVATE INPUT FIELDS
    # ==========================================

    bitelevate_fields = driver.find_elements(
        By.XPATH,
        "//input | //textarea | //select"
    )

    record(
        "TC17 BitElevate Fields",
        "INFO",
        f"Fields found: {len(bitelevate_fields)}"
    )


    # ==========================================
    # TC18: CAREERS PAGE
    # ==========================================

    open_page("https://www.cynbit.in/careers")

    record(
        "TC18 Careers Page",
        "PASS",
        driver.current_url
    )


    # ==========================================
    # TC19: BLOG PAGE
    # ==========================================

    open_page("https://www.cynbit.in/blog")

    record(
        "TC19 Blog Page",
        "PASS",
        driver.current_url
    )


    # ==========================================
    # TC20: CASE STUDIES PAGE
    # ==========================================

    open_page("https://www.cynbit.in/case-studies")

    record(
        "TC20 Case Studies Page",
        "PASS",
        driver.current_url
    )


    # ==========================================
    # TC21: FOOTER VISIBILITY
    # ==========================================

    footers = driver.find_elements(By.TAG_NAME, "footer")

    if footers and any(f.is_displayed() for f in footers):

        record(
            "TC21 Footer Visibility",
            "PASS",
            "Footer visible"
        )

    else:

        record(
            "TC21 Footer Visibility",
            "FAIL",
            "Footer not found or hidden"
        )


    # ==========================================
    # TC22: RESPONSIVE TESTING
    # ==========================================

    print("\n========== RESPONSIVE TESTING ==========")

    screen_sizes = [
        ("Desktop", 1366, 768),
        ("Tablet", 768, 1024),
        ("Mobile", 390, 844)
    ]

    for device, width, height in screen_sizes:

        driver.set_window_size(width, height)

        open_page(BASE_URL)

        time.sleep(2)

        viewport_width = driver.execute_script(
            "return window.innerWidth"
        )

        page_width = driver.execute_script(
            "return document.documentElement.scrollWidth"
        )

        if page_width <= viewport_width:

            record(
                f"TC22 Responsive {device}",
                "PASS",
                f"Viewport: {viewport_width}, Page: {page_width}"
            )

        else:

            record(
                f"TC22 Responsive {device}",
                "FAIL",
                f"Viewport: {viewport_width}, Page: {page_width}"
            )


finally:

    # ==========================================
    # FINAL REPORT
    # ==========================================

    print("\n========== FINAL AUDIT SUMMARY ==========")

    passed = sum(
        1 for result in results
        if result["status"] == "PASS"
    )

    failed = sum(
        1 for result in results
        if result["status"] == "FAIL"
    )

    info = sum(
        1 for result in results
        if result["status"] == "INFO"
    )

    errors = sum(
        1 for result in results
        if result["status"] == "ERROR"
    )

    print("Total Results:", len(results))
    print("Passed:", passed)
    print("Failed:", failed)
    print("Information:", info)
    print("Errors:", errors)

    with open(
            "../reports/cynbit_complete_audit_report.txt",
        "w",
        encoding="utf-8"
    ) as report:

        for result in results:

            report.write(
                f"{result['status']} | "
                f"{result['test']} | "
                f"{result['details']}\n"
            )

        report.write("\n========== SUMMARY ==========\n")
        report.write(f"Total: {len(results)}\n")
        report.write(f"Passed: {passed}\n")
        report.write(f"Failed: {failed}\n")
        report.write(f"Info: {info}\n")
        report.write(f"Errors: {errors}\n")

    print("\nReport saved: cynbit_complete_audit_report.txt")

    driver.quit()
