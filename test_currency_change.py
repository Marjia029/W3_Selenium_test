from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
import traceback

def test_currency_change_for_cards(driver, url):
    try:
        # Open the webpage
        driver.get(url)

        # Wait for the price elements to load
        print("Waiting for price elements...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-price-value'))
        )
        price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
        initial_prices = [elem.text for elem in price_elements]
        print(f"Found {len(initial_prices)} price elements.")

        # Print initial prices
        print("Initial Prices:")
        for i, price in enumerate(initial_prices):
            print(f"Card {i + 1}: {price}")

        # Detailed page source investigation
        print("\nInvestigating page structure...")
        # Find potential currency dropdown elements
        potential_dropdowns = driver.find_elements(By.XPATH, "//*[contains(@id, 'currency') or contains(@class, 'currency')]")
        print(f"Found {len(potential_dropdowns)} potential currency-related elements:")
        for i, elem in enumerate(potential_dropdowns):
            print(f"{i+1}. ID: {elem.get_attribute('id')}, Class: {elem.get_attribute('class')}, Visible: {elem.is_displayed()}")

        # Find the currency dropdown more flexibly
        print("\nTrying multiple methods to find currency dropdown...")
        dropdown_locators = [
            (By.ID, 'js-currency-sort-footer'),
            (By.XPATH, "//select[contains(@id, 'currency')]"),
            (By.XPATH, "//div[contains(@class, 'currency-selector')]"),
            (By.XPATH, "//*[contains(translate(text(), 'USD', 'usd'), 'usd')]")
        ]

        dropdown_element = None
        for locator in dropdown_locators:
            try:
                dropdown_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(locator)
                )
                print(f"Found dropdown using locator: {locator}")
                break
            except TimeoutException:
                print(f"Could not find dropdown with locator: {locator}")

        if dropdown_element is None:
            print("Could not find currency dropdown. Saving page source for investigation.")
            with open('page_source.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            return

        # Scroll to the dropdown
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_element)
        time.sleep(2)

        # Multiple interaction attempts
        interaction_methods = [
            lambda: dropdown_element.click(),
            lambda: ActionChains(driver).move_to_element(dropdown_element).click().perform(),
            lambda: driver.execute_script("arguments[0].click();", dropdown_element)
        ]

        for method in interaction_methods:
            try:
                method()
                print("Successfully clicked dropdown using a method.")
                
                # Wait for USD option
                usd_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(translate(text(), 'USD', 'usd'), 'usd')]"))
                )
                
                # Try clicking USD option
                usd_option.click()
                print("USD option clicked.")
                
                break
            except Exception as e:
                print(f"Interaction method failed: {e}")
                continue

        # Wait for prices to update
        WebDriverWait(driver, 30).until(
            lambda d: any('$' in elem.text for elem in d.find_elements(By.CLASS_NAME, 'js-price-value'))
        )

        # Capture and print updated prices
        updated_price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
        updated_prices = [elem.text for elem in updated_price_elements]

        print("Updated Prices (After Currency Change):")
        for i, price in enumerate(updated_prices):
            print(f"Card {i + 1}: {price}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        
        # Save page source for debugging
        with open('error_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        # Take screenshot
        driver.save_screenshot("error_screenshot.png")

# Main execution
if __name__ == "__main__":
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    #options.add_argument("--window-size=1920,1080")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        test_currency_change_for_cards(driver, "https://www.alojamiento.io/")
    finally:
        driver.quit()