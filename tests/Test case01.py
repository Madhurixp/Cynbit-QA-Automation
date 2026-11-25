
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# BROWSER SETUP

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()

BASE_URL = "https://www.cynbit.in"

results = []

# FUNCTION TO PRINT TEST RESULTS

def report(test_name, status):

    if status:
        print("PASSED:", test_name)
    else:
        print("FAILED:", test_name)

    results.append((test_name, status))


try:


    # TC01 - TC05: VERIFY MAIN PAGES

    pages = [
        ("Homepage", "/"),
        ("Services", "/services"),
        ("Products", "/products"),
        ("Contact", "/contact"),
        ("BitElevate", "/bitelevate")
    ]

    for page_name, path in pages:

        driver.get(BASE_URL + path)

        time.sleep(3)

        actual_url = driver.current_url.rstrip("/")
        expected_url = (BASE_URL + path).rstrip("/")

        page_title = driver.title
        headings = driver.find_elements(By.TAG_NAME, "h1")

        print("\nChecking:", page_name)
        print("Page Title:", page_title)
        print("Current URL:", actual_url)

        report(
            page_name + " page loads correctly",
            actual_url == expected_url and
            page_title != "" and
            len(headings) > 0
        )

    # TC06: VERIFY CYNBIT LOGO

    driver.get(BASE_URL)

    time.sleep(3)

    logo = driver.find_elements(
        By.XPATH, "//img[@alt='Cynbit Logo']"
    )

    if len(logo) > 0:

        report(
            "Cynbit logo is visible",
            logo[0].is_displayed()
        )

    else:

        report("Cynbit logo is present", False)

    # TC07: VERIFY NAVIGATION LINKS

    navigation_links = driver.find_elements(
        By.CSS_SELECTOR, "nav a[href]"
    )

    print("\nNavigation links found:", len(navigation_links))

    report(
        "Navigation links are available",
        len(navigation_links) > 0
    )

    for link in navigation_links:

        print(
            link.text.strip(),
            "->",
            link.get_attribute("href")
        )


    # TC08: VERIFY INTERNAL LINKS

    all_links = driver.find_elements(
        By.CSS_SELECTOR, "a[href]"
    )

    internal_links = []

    for link in all_links:

        href = link.get_attribute("href")

        if href and "cynbit.in" in href:
            internal_links.append(href)

    report(
        "Internal links are available",
        len(internal_links) > 0
    )

    print("Internal links found:", len(internal_links))


    # TC09 - TC13: CHECK IMAGES ON PAGES

    for page_name, path in pages:

        driver.get(BASE_URL + path)

        time.sleep(2)

        # Scroll to load lazy-loaded images
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(2)

        broken_images = driver.execute_script("""
            return Array.from(document.images)
                .filter(img => img.complete && img.naturalWidth === 0)
                .map(img => img.src);
        """)

        print("\nImages checked on:", page_name)

        if len(broken_images) == 0:

            report(page_name + " images loaded", True)

        else:

            report(page_name + " images loaded", False)

            print("Broken image URLs:", broken_images)

    # TC14: CONTACT FORM CHECK

    driver.get(BASE_URL + "/contact")

    time.sleep(3)

    contact_forms = driver.find_elements(
        By.TAG_NAME, "form"
    )

    contact_fields = driver.find_elements(
        By.CSS_SELECTOR, "input, textarea, select"
    )

    print("\nContact forms:", len(contact_forms))
    print("Contact fields:", len(contact_fields))

    report(
        "Contact form fields are available",
        len(contact_fields) >= 3
    )

    # TC15: PRODUCT DEMO FORM CHECK

    driver.get(BASE_URL + "/products")

    time.sleep(3)

    demo_fields = driver.find_elements(
        By.CSS_SELECTOR, "input, textarea, select"
    )

    print("\nProduct demo fields:", len(demo_fields))

    report(
        "Product demo form fields are available",
        len(demo_fields) >= 3
    )

    # TC16 - TC18: RESPONSIVE CHECK

    driver.get(BASE_URL)

    time.sleep(3)

    screen_sizes = [
        ("Desktop", 1366, 768),
        ("Tablet", 768, 1024),
        ("Mobile", 390, 844)
    ]

    for device, width, height in screen_sizes:

        driver.set_window_size(width, height)

        time.sleep(2)

        horizontal_overflow = driver.execute_script(
            "return document.documentElement.scrollWidth > window.innerWidth;"
        )

        report(
            device + " layout has no horizontal overflow",
            not horizontal_overflow
        )

    # FINAL TEST REPORT

    print("\n================================")
    print("       CYNBIT QA TEST REPORT")
    print("================================")

    passed = sum(1 for name, status in results if status)
    failed = sum(1 for name, status in results if not status)
    total = len(results)

    print("Total Tests:", total)
    print("Passed:", passed)
    print("Failed:", failed)

    if failed == 0:
        print("OVERALL RESULT: ALL CHECKS PASSED")
    else:
        print("OVERALL RESULT: SOME CHECKS FAILED")

    print("================================")


finally:

    driver.quit()
