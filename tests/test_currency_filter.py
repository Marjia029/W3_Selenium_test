from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_currency_filter(driver):
    """
    Test currency change functionality on the property page.
    
    Returns:
    - Boolean: Whether the currency change test passed
    - String: Comments about the test results
    """
    try:
        # Capture the initial value of the availability price
        availability_price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'js-default-price'))
        )
        initial_availability_price = availability_price_element.text.strip()

        # Wait for the price elements to load in cards
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-price-value'))
        )
        price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
        initial_prices = [elem.text for elem in price_elements]

        # Scroll to the footer section to locate the currency dropdown
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'js-currency-sort-footer'))
        )
        footer_currency_element = driver.find_element(By.ID, 'js-currency-sort-footer')
        driver.execute_script("arguments[0].scrollIntoView(true);", footer_currency_element)
        time.sleep(1)  # Wait for the scroll to complete

        # Click on the currency dropdown
        currency_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, 'js-currency-sort-footer'))
        )
        currency_dropdown.click()

        # Fetch all available currency options
        currency_options = driver.find_elements(By.XPATH, "//div[@class='footer-section']//div[@class='footer-currency-dd']//ul[@class='select-ul']//li")

        # Track overall test result
        overall_test_passed = True
        test_comments = []

        # Test the first currency option (skipping the first if it's the default)
        if len(currency_options) > 1:
            currency_option = currency_options[1]  # Select the second option
            currency_text = currency_option.text.strip()

            # Scroll to and click on the currency option
            driver.execute_script("arguments[0].scrollIntoView(true);", currency_option)
            time.sleep(1)
            try:
                currency_option.click()
            except Exception:
                driver.execute_script("arguments[0].click();", currency_option)

            # Wait for the availability price to update
            WebDriverWait(driver, 50).until(
                EC.text_to_be_present_in_element((By.ID, 'js-default-price'), currency_text.split()[0])
            )
            updated_availability_price = availability_price_element.text.strip()

            # Wait for the prices to update in the cards
            WebDriverWait(driver, 50).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'js-price-value'), currency_text.split()[0])
            )
            updated_price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
            updated_prices = [elem.text for elem in updated_price_elements]

            # Compare initial and updated prices
            price_changes = []
            for i in range(len(initial_prices)):
                if initial_prices[i] == updated_prices[i]:
                    price_changes.append(False)
                    overall_test_passed = False
                else:
                    price_changes.append(True)

            # Check availability price change
            availability_price_changed = currency_text.split()[0] in updated_availability_price

            # Prepare comments
            comments_list = [
                f"Tested currency change to {currency_text}",
                f"Availability Price Change: {'Yes' if availability_price_changed else 'No'}",
                f"Price Changes: {sum(price_changes)}/{len(price_changes)} card prices updated",
            ]
            test_comments = "; ".join(comments_list)

        else:
            # Not enough currency options to test
            overall_test_passed = False
            test_comments = "Insufficient currency options to perform test"

        return overall_test_passed, test_comments

    except Exception as e:
        return False, f"Currency filter test failed: {str(e)}"