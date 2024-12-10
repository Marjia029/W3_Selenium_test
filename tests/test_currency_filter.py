from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_currency_filter(driver):
    """
    Test currency change functionality across all available currency options.

    Returns:
    - Boolean: Whether the currency change test passed.
    - String: Detailed comments about the test results.
    """
    try:
        # Capture the initial value of the availability price
        availability_price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'js-default-price'))
        )
        initial_availability_price = availability_price_element.text.strip()
        print(f"Initial Availability Price: {initial_availability_price}")

        # Wait for the price elements to load in cards
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-price-value'))
        )
        price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
        total_cards = len(price_elements)
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
        print(f"Found {len(currency_options)} currency options.")
        
        # Prepare overall test result tracking
        overall_test_passed = True
        comprehensive_comments = []

        # Skip the first currency option (likely the default)
        for currency_option in currency_options[0:]:
            # Reset currency dropdown
            currency_dropdown = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.ID, 'js-currency-sort-footer'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", currency_dropdown)
            currency_dropdown.click()

            # Get current currency text
            currency_text = currency_option.text.strip()
            
            # Skip empty options
            if not currency_text:
                continue

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

            # Count the number of cards with changed prices
            changed_count = sum(1 for i in range(total_cards) if initial_prices[i] != updated_prices[i])

            # Prepare comments for this currency
            currency_test_passed = changed_count > 0
            comprehensive_comments.append({
                'currency': currency_text,
                'availability_price_changed': currency_text.split()[0] in updated_availability_price,
                'total_cards': total_cards,
                'changed_cards': changed_count
            })

            # Update overall test result
            if not currency_test_passed:
                overall_test_passed = False

            # Update initial prices for the next iteration
            initial_availability_price = updated_availability_price
            initial_prices = updated_prices

        # Format comments for output
        formatted_comments = [
            f"Currency: {result['currency']}; Changed Cards: {result['changed_cards']} of {result['total_cards']}; "
            f"Availability Price Change: {result['availability_price_changed']}"
            for result in comprehensive_comments
        ]

        final_comments = " \n ".join(formatted_comments)

        return overall_test_passed, final_comments

    except Exception as e:
        return False, f"Currency filter test failed: {str(e)}"
