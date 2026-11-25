
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# ==============================
# BROWSER SETUP
# ==============================

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()
wait = WebDriverWait(driver, 10)

BASE_URL = "https://www.cynbit.in/"

results = []


# ==============================
# RESULT FUNCTION
# ==============================

def log_result(test_name, status, details=""):
    message = f"{status}: {test_name} - {details}"
    print(message)
    results.append((test_name, status, details))


# ==============================
# TC01 - HOMEPAGE LOADING
# ==============================

driver.get(BASE_URL)
time.sleep(3)

if driver.current_url == BASE_URL:
    log_result("TC01 Homepage Loading", "PASS", driver.current_url)
else:
    log_result("TC01 Homepage Loading", "FAIL", driver.current_url)


# ==============================
# TC02 - PAGE TITLE
# ==============================

if driver.title:
    log_result("TC02 Page Title", "PASS", driver.title)
else:
    log_result("TC02 Page Title", "FAIL", "Page title is empty")


# ==============================
# TC03 - LOGO VISIBILITY
# ==============================

try:
    logo = driver.find_element(
        By.XPATH, "//img[@alt='Cynbit Logo']"
    )

    if logo.is_displayed():
        log_result("TC03 Logo Visibility", "PASS", "Logo visible")
    else:
        log_result("TC03 Logo Visibility", "FAIL", "Logo not visible")

except Exception as e:
    log_result("TC03 Logo Visibility", "FAIL", str(e))


# ==============================
# TC04 - HEADER VISIBILITY
# ==============================

try:
    header = driver.find_element(By.TAG_NAME, "header")

    if header.is_displayed():
        log_result("TC04 Header Visibility", "PASS", "Header visible")
    else:
        log_result("TC04 Header Visibility", "FAIL", "Header not visible")

except Exception as e:
    log_result("TC04 Header Visibility", "FAIL", str(e))


# ==============================
# TC05 - NAVIGATION MENU
# ==============================

try:
    navigation_links = driver.find_elements(
        By.XPATH, "//header//a"
    )

    visible_links = [
        link for link in navigation_links
        if link.is_displayed()
    ]

    log_result(
        "TC05 Navigation Menu",
        "PASS",
        f"{len(visible_links)} visible navigation links"
    )

except Exception as e:
    log_result("TC05 Navigation Menu", "FAIL", str(e))


# ==============================
# TC06 - INTERNAL LINK DISCOVERY
# ==============================

internal_links = set()

links = driver.find_elements(By.TAG_NAME, "a")

for link in links:
    href = link.get_attribute("href")

    if href and href.startswith(BASE_URL):
        internal_links.add(href.split("#")[0])

log_result(
    "TC06 Internal Link Discovery",
    "INFO",
    f"{len(internal_links)} internal links discovered"
)


# ==============================
# TC07 - INTERNAL LINK STATUS
# ==============================

for url in sorted(internal_links):

    try:
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            log_result(
                "TC07 Link Status",
                "PASS",
                f"{url} - HTTP {response.status_code}"
            )
        else:
            log_result(
                "TC07 Link Status",
                "FAIL",
                f"{url} - HTTP {response.status_code}"
            )

    except requests.RequestException as e:
        log_result("TC07 Link Status", "FAIL", f"{url} - {e}")


# ==============================
# TC08 - BROWSER PAGE NAVIGATION
# ==============================

for url in sorted(internal_links):

    try:
        driver.get(url)
        time.sleep(1)

        if driver.find_element(By.TAG_NAME, "body"):
            log_result(
                "TC08 Page Navigation",
                "PASS",
                url
            )
        else:
            log_result(
                "TC08 Page Navigation",
                "FAIL",
                url
            )

    except Exception as e:
        log_result(
            "TC08 Page Navigation",
            "FAIL",
            f"{url} - {e}"
        )


# ==============================
# TC09 - IMAGE URL STATUS
# ==============================

driver.get(BASE_URL)
time.sleep(2)

images = driver.find_elements(By.TAG_NAME, "img")

for index, img in enumerate(images, start=1):

    image_url = img.get_attribute("src")

    if image_url:

        try:
            response = requests.get(image_url, timeout=15)

            if response.status_code == 200:
                log_result(
                    "TC09 Image URL",
                    "PASS",
                    f"Image {index} - HTTP {response.status_code}"
                )
            else:
                log_result(
                    "TC09 Image URL",
                    "FAIL",
                    f"Image {index} - HTTP {response.status_code}"
                )

        except requests.RequestException as e:
            log_result(
                "TC09 Image URL",
                "FAIL",
                f"Image {index} - {e}"
            )


# ==============================
# TC10 - CONTACT PAGE
# ==============================

try:
    driver.get(BASE_URL + "contact")
    time.sleep(2)

    if "contact" in driver.current_url:
        log_result(
            "TC10 Contact Page",
            "PASS",
            driver.current_url
        )
    else:
        log_result(
            "TC10 Contact Page",
            "FAIL",
            driver.current_url
        )

except Exception as e:
    log_result("TC10 Contact Page", "FAIL", str(e))


# ==============================
# TC11 - CONTACT FORM COUNT
# ==============================

forms = driver.find_elements(By.TAG_NAME, "form")

log_result(
    "TC11 Contact Forms",
    "INFO",
    f"Forms found: {len(forms)}"
)


# ==============================
# TC12 - CONTACT INPUT FIELDS
# ==============================

input_fields = driver.find_elements(
    By.XPATH, "//input | //textarea"
)

log_result(
    "TC12 Contact Input Fields",
    "INFO",
    f"Fields found: {len(input_fields)}"
)

for field in input_fields:

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


# ==============================
# TC13 - CONTACT EMAIL AND PHONE
# ==============================

contact_links = driver.find_elements(
    By.XPATH, "//a[starts-with(@href,'mailto:') or starts-with(@href,'tel:')]"
)

if contact_links:
    for link in contact_links:
        log_result(
            "TC13 Contact Link",
            "INFO",
            link.get_attribute("href")
        )
else:
    log_result(
        "TC13 Contact Link",
        "FAIL",
        "No email or phone links found"
    )


# ==============================
# TC14 - PRODUCTS PAGE
# ==============================

driver.get(BASE_URL + "products")
time.sleep(2)

if "products" in driver.current_url:
    log_result(
        "TC14 Products Page",
        "PASS",
        driver.current_url
    )
else:
    log_result(
        "TC14 Products Page",
        "FAIL",
        driver.current_url
    )


# ==============================
# TC15 - PRODUCTS PAGE FIELDS
# ==============================

product_fields = driver.find_elements(
    By.XPATH, "//input | //textarea | //button"
)

log_result(
    "TC15 Products Fields",
    "INFO",
    f"Fields found: {len(product_fields)}"
)


# ==============================
# TC16 - BITELEVATE PAGE
# ==============================

driver.get(BASE_URL + "bitelevate")
time.sleep(2)

if "bitelevate" in driver.current_url:
    log_result(
        "TC16 BitElevate Page",
        "PASS",
        driver.current_url
    )
else:
    log_result(
        "TC16 BitElevate Page",
        "FAIL",
        driver.current_url
    )


# ==============================
# TC17 - BITELEVATE PAGE FIELDS
# ==============================

bitelevate_fields = driver.find_elements(
    By.XPATH, "//input | //textarea | //button"
)

log_result(
    "TC17 BitElevate Fields",
    "INFO",
    f"Fields found: {len(bitelevate_fields)}"
)


# ==============================
# TC18 - CAREERS PAGE
# ==============================

driver.get(BASE_URL + "careers")
time.sleep(2)

if "careers" in driver.current_url:
    log_result(
        "TC18 Careers Page",
        "PASS",
        driver.current_url
    )
else:
    log_result(
        "TC18 Careers Page",
        "FAIL",
        driver.current_url
    )


# ==============================
# TC19 - BLOG PAGE
# ==============================

driver.get(BASE_URL + "blog")
time.sleep(2)

if "blog" in driver.current_url:
    log_result(
        "TC19 Blog Page",
        "PASS",
        driver.current_url
    )
else:
    log_result(
        "TC19 Blog Page",
        "FAIL",
        driver.current_url
    )


# ==============================
# TC20 - CASE STUDIES PAGE
# ==============================

driver.get(BASE_URL + "case-studies")
time.sleep(2)

if "case-studies" in driver.current_url:
    log_result(
        "TC20 Case Studies Page",
        "PASS",
        driver.current_url
    )
else:
    log_result(
        "TC20 Case Studies Page",
        "FAIL",
        driver.current_url
    )


# ==============================
# TC21 - FOOTER VISIBILITY
# ==============================

try:
    footer = driver.find_element(By.TAG_NAME, "footer")

    if footer.is_displayed():
        log_result(
            "TC21 Footer Visibility",
            "PASS",
            "Footer visible"
        )
    else:
        log_result(
            "TC21 Footer Visibility",
            "FAIL",
            "Footer not visible"
        )

except Exception as e:
    log_result("TC21 Footer Visibility", "FAIL", str(e))


# ==============================
# TC22 - RESPONSIVE TESTING
# ==============================

viewports = [
    ("Desktop", 1366, 768),
    ("Tablet", 768, 1024),
    ("Mobile", 390, 844)
]

for device, width, height in viewports:

    driver.get(BASE_URL)
    time.sleep(2)

    driver.execute_cdp_cmd(
        "Emulation.setDeviceMetricsOverride",
        {
            "width": width,
            "height": height,
            "deviceScaleFactor": 1,
            "mobile": device == "Mobile"
        }
    )

    time.sleep(2)

    dimensions = driver.execute_script("""
        return {
            viewport: window.innerWidth,
            page: document.documentElement.scrollWidth,
            body: document.body.scrollWidth
        };
    """)

    if dimensions["page"] <= dimensions["viewport"]:
        log_result(
            f"TC22 Responsive - {device}",
            "PASS",
            f"Viewport {dimensions['viewport']} Page {dimensions['page']}"
        )
    else:
        log_result(
            f"TC22 Responsive - {device}",
            "FAIL",
            f"Viewport {dimensions['viewport']} Page {dimensions['page']}"
        )

driver.execute_cdp_cmd(
    "Emulation.clearDeviceMetricsOverride", {}
)


# ==============================
# FINAL SUMMARY
# ==============================

passed = sum(1 for result in results if result[1] == "PASS")
failed = sum(1 for result in results if result[1] == "FAIL")
information = sum(1 for result in results if result[1] == "INFO")

print("\n========== FINAL TEST SUMMARY ==========")
print("Total Results:", len(results))
print("Passed:", passed)
print("Failed:", failed)
print("Information:", information)


# ==============================
# SAVE AUDIT REPORT
# ==============================

with open(
        "../reports/cynbit_complete_audit_report.txt",
    "w",
    encoding="utf-8"
) as report:

    report.write("CYNBIT WEBSITE QA AUDIT REPORT\n")
    report.write("=" * 45 + "\n\n")

    for test_name, status, details in results:
        report.write(
            f"{status}: {test_name} - {details}\n"
        )

    report.write("\n========== SUMMARY ==========\n")
    report.write(f"Total Results: {len(results)}\n")
    report.write(f"Passed: {passed}\n")
    report.write(f"Failed: {failed}\n")
    report.write(f"Information: {information}\n")

print("\nReport saved as cynbit_complete_audit_report.txt")


# ==============================
# CLOSE BROWSER
# ==============================

driver.quit()
