import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openpyxl import load_workbook

def test_currency_filter(driver):
    """
    Test currency change functionality across all available currency options.
    
    Returns:
    - Boolean: Whether the currency change test passed.
    - String: Detailed comments about the test results.
    """
    try:
        # Wait for the initial card prices to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-price-value'))
        )

        # Capture the initial card prices
        price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
        total_cards = len(price_elements)
        initial_prices = [elem.text.strip() for elem in price_elements]

        # Prepare data storage for all price changes
        price_changes = []

        # Locate the currency dropdown
        footer_currency_element = driver.find_element(By.ID, 'js-currency-sort-footer')
        driver.execute_script("arguments[0].scrollIntoView(true);", footer_currency_element)
        time.sleep(1)

        # Fetch all currency options
        original_currency_options = driver.find_elements(
            By.XPATH, "//div[@class='footer-section']//ul[@class='select-ul']//li"
        )

        # Process each currency option
        for currency_index in range(len(original_currency_options)):
            # Re-fetch currency options to avoid stale element issues
            currency_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'js-currency-sort-footer'))
            )
            currency_dropdown.click()
            time.sleep(1)  # Allow the dropdown to stabilize
            currency_options = driver.find_elements(
                By.XPATH, "//div[@class='footer-section']//ul[@class='select-ul']//li"
            )

            # Select the current currency
            currency_option = currency_options[currency_index]
            currency_text = currency_option.text.strip()

            if not currency_text:
                continue

            # Click the currency option
            driver.execute_script("arguments[0].scrollIntoView(true);", currency_option)
            time.sleep(1)
            currency_option.click()

            # Wait for prices to update
            WebDriverWait(driver, 50).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-price-value'))
            )
            updated_prices = [elem.text.strip() for elem in driver.find_elements(By.CLASS_NAME, 'js-price-value')]

            # Record changes for each card
            for idx in range(total_cards):
                price_changes.append({
                    "Currency": currency_text,
                    "Card No": idx + 1,
                    "Initial Price": initial_prices[idx],
                    "Updated Price": updated_prices[idx]
                })

            # Update initial prices for the next iteration
            initial_prices = updated_prices

        # Save results to a new Excel sheet
        report_path = "reports/test_report.xlsx"
        sheet_name = "CurrencyPriceChanges"
        df = pd.DataFrame(price_changes)

        try:
            with pd.ExcelWriter(report_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        except FileNotFoundError:
            with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        return True, f"Currency filter test passed. Results saved to {report_path}, sheet '{sheet_name}'."

    except Exception as e:
        return False, f"Currency filter test failed: {str(e)}"
