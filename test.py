import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

import time


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.alojamiento.io/")
print ("Title of the page: " , driver.title)

h1_tags = driver.find_elements(By.TAG_NAME, "h1")

if h1_tags:
    print(f"✅ The page contains {len(h1_tags)} <h1> tag(s).")
else:
    print("❌ The page does not contain any <h1> tags.")


# Function to check the sequence of heading tags
def check_heading_sequence(driver):
    # Find all heading tags on the page
    heading_tags = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6")
    
    if not heading_tags:
        print("❌ No heading tags found on the page.")
        return

    # Extract the heading levels
    heading_levels = [int(tag.tag_name[1]) for tag in heading_tags]

    # Print the headings and their levels
    # print("Headings on the page:")
    # for tag in heading_tags:
    #     print(f"{tag.tag_name}: {tag.text.strip()}")

    # Check if the sequence is non-decreasing
    is_valid_sequence = all(heading_levels[i] <= heading_levels[i + 1] for i in range(len(heading_levels) - 1))
    
    if is_valid_sequence:
        print("✅ The headings are in the correct sequence.")
    else:
        print("❌ The headings are not in the correct sequence.")

check_heading_sequence(driver)

#Checkiong Image alt attributes
images = driver.find_elements(By.TAG_NAME, "img")
failed_images = []

for idx, img in enumerate(images, 1):
    alt_attribute = img.get_attribute("alt")
    if not alt_attribute:  # If alt attribute is missing
        failed_images.append(idx)

# Output result
if failed_images:
    print(f"FAIL: Images {failed_images} are missing the alt attribute.")
else:
    print("PASS: All images have the alt attribute.")


# Check URL status codes for all links
links = driver.find_elements(By.TAG_NAME, "a")
failed_urls = []

for link in links:
    url = link.get_attribute("href")
    if url:  # Skip empty URLs
        try:
            response = requests.get(url)
            if response.status_code == 404:  # If status code is 404
                failed_urls.append(url)
        except requests.exceptions.RequestException as e:
            print(f"Error checking URL {url}: {e}")

# Output result for URLs
if failed_urls:
    print(f"FAIL: The following URLs returned a 404 status code: {failed_urls}")
else:
    print("PASS: All URLs returned a valid status code.")



try:
    # Locate the dropdown element
    currency_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
    )
    currency_dropdown.click()  # Open the dropdown menu

    # Wait for the options to be visible
    usd_currency = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//li[@data-currency-country='US']"))
    )
    usd_currency.click()  # Select the USD option

    # Verify the currency change
    selected_currency = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='js-currency-sort-footer']//p"))
    )
    print("Selected currency:", selected_currency.text)

except TimeoutException:
    print("Element could not be found or was not interactable within the time limit.")
except ElementNotInteractableException:
    print("Element is not interactable. Check its visibility and position.")


driver.quit()
print ("Driver stopped")