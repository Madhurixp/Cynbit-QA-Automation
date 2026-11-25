
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

try:
    driver.get("https://www.cynbit.in/")
    time.sleep(4)

    print("\n========== RESPONSIVE DESIGN TESTING ==========")

    devices = [
        ("Desktop", 1366, 768, False),
        ("Tablet", 768, 1024, False),
        ("Mobile", 390, 844, True)
    ]

    for name, width, height, mobile in devices:

        driver.execute_cdp_cmd(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
                "mobile": mobile
            }
        )

        time.sleep(3)

        dimensions = driver.execute_script("""
            return {
                viewportWidth: document.documentElement.clientWidth,
                pageWidth: document.documentElement.scrollWidth,
                bodyWidth: document.body.scrollWidth,
                viewportHeight: window.innerHeight
            };
        """)

        viewport = dimensions["viewportWidth"]
        page = dimensions["pageWidth"]

        print("\nDevice:", name)
        print("Expected Width:", width)
        print("Actual Viewport Width:", viewport)
        print("Page Width:", page)
        print("Body Width:", dimensions["bodyWidth"])

        if page <= viewport:
            print("PASS: No horizontal overflow detected")
        else:
            print("FAIL: Horizontal overflow detected")

        driver.save_screenshot(
            name.lower() + "_responsive.png"
        )

    print("\nResponsive testing completed.")

finally:
    driver.quit()
