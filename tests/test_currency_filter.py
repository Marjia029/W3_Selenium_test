from selenium.webdriver.common.by import By
def test_currency_filter(driver):
    # Locate the currency filter and property tiles (you may need to adjust the selectors)
    currency_filter = driver.find_element(By.ID,"currency-filter")
    currency_filter.click()  # Assume it changes the currency when clicked
    property_tiles = driver.find_elements_by_class_name("property-tile")

    # Check if currency in property tiles has changed
    currencies = [tile.text for tile in property_tiles]
    if "USD" not in currencies:  # Example check, adjust as needed
        return False, "Currency not changed as expected"
    
    return True, "Currency filter is working correctly"
