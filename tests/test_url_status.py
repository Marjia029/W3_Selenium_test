import requests
from selenium.webdriver.common.by import By

def test_url_status(driver):
    links = driver.find_elements(By.TAG_NAME, "a")
    failed_urls = []
    ssl_error_urls = []


    for link in links:
        url = link.get_attribute("href")
        if url:
            try:
                response = requests.get(url)
                if response.status_code == 404:
                    failed_urls.append(url)
            except requests.exceptions.RequestException:
                ssl_error_urls.append(url)
    
    if failed_urls:
        return False, f"404 errors found for URLs: {failed_urls}"
    elif ssl_error_urls:
        return True, f"No 404 urls, but SSL errors found for URLs: {ssl_error_urls}"
    
    return True, "All URLs returned valid status codes"
