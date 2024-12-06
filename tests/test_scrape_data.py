from utils.data_scraper import scrape_script_data

def test_scrape_data(driver):
    data = scrape_script_data(driver)
    # Customize the expected values as per the page structure
    if data["country_code"] == "Not Found":
        return False, "Country code not found in script data"
    return True, f"Scraped data: {data}"
