import requests
from selenium.webdriver.common.by import By
import pandas as pd
from openpyxl import load_workbook


def test_url_status(driver):
    """
    Test all links on the page for their status code and save 404 errors.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        tuple: (bool, str) - Test result (pass/fail) and comments.
    """
    links = driver.find_elements(By.TAG_NAME, "a")
    failed_urls = []
    ssl_error_urls = []

    for link in links:
        url = link.get_attribute("href")
        if url:
            try:
                response = requests.get(url)
                if response.status_code == 404:
                    failed_urls.append({"URL": url, "Status Code": 404})
            except requests.exceptions.RequestException:
                ssl_error_urls.append(url)

    if failed_urls:
        # Save 404 errors to a new Excel sheet
        report_path = "reports/test_report.xlsx"
        sheet_name = "404Errors"
        df = pd.DataFrame(failed_urls)

        try:
            with pd.ExcelWriter(report_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        except FileNotFoundError:
            with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        return False, f"404 errors found for URLs. Details saved to {report_path}, sheet '{sheet_name}'."

    if ssl_error_urls:
        return True, f"No 404 URLs, found {len(ssl_error_urls)} not accessible urls."

    return True, "All URLs returned valid status codes"
